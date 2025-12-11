import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.followup import FollowUp
from app.models.emergency import EmergencyReport
from app.crud import followup_crud, report_crud
from app.services.notification_service import NotificationService
from app.services.websocket_service import manager

logger = logging.getLogger(__name__)


async def schedule_checkin(
    report_id: int,
    hours: int,
    db: Session,
    notes: str = None
) -> FollowUp:
    """
    Schedule a follow-up check-in for an emergency report.
    
    Args:
        report_id: ID of the emergency report
        hours: Number of hours to delay before check-in
        db: Database session
        notes: Optional notes for the follow-up
    
    Returns:
        FollowUp object created in database
    """
    try:
        # Validate report exists
        report = report_crud.get_report(db=db, report_id=report_id)
        if not report:
            raise ValueError(f"Emergency report {report_id} not found")
        
        # Calculate scheduled time
        scheduled_time = datetime.utcnow() + timedelta(hours=hours)
        
        # Create follow-up entry
        follow_up = followup_crud.create_followup(
            db=db,
            emergency_report_id=report_id,
            user_id=report.user_id,
            status="PENDING",
            scheduled_time=scheduled_time,
            follow_up_type="MANUAL",
            notes=notes or f"Manual follow-up scheduled for {hours} hours"
        )
        
        logger.info(
            f"Follow-up {follow_up.id} scheduled for report {report_id} "
            f"at {scheduled_time} (in {hours} hours)"
        )
        
        # Queue notification to be sent at scheduled time
        await queue_followup_notification(follow_up, db)
        
        return follow_up
        
    except Exception as e:
        logger.error(f"Failed to schedule follow-up for report {report_id}: {str(e)}")
        raise


async def process_checkin(
    follow_up_id: int,
    user_id: int,
    response: str,
    db: Session
) -> FollowUp:
    """
    Process a check-in response from a user.
    
    Args:
        follow_up_id: ID of the follow-up
        user_id: ID of the user checking in
        response: User's response to the check-in
        db: Database session
    
    Returns:
        Updated FollowUp object
    """
    try:
        # Retrieve follow-up
        follow_up = followup_crud.get_followup(db=db, followup_id=follow_up_id)
        if not follow_up:
            raise ValueError(f"Follow-up {follow_up_id} not found")
        
        # Authorization: user must own the follow-up
        if follow_up.user_id != user_id:
            raise PermissionError(f"User {user_id} not authorized for follow-up {follow_up_id}")
        
        # Update follow-up status
        follow_up.status = "COMPLETED"
        follow_up.completed_at = datetime.utcnow()
        follow_up.user_response = response
        
        db.commit()
        db.refresh(follow_up)
        
        logger.info(
            f"Follow-up {follow_up_id} completed by user {user_id} "
            f"with response: {response}"
        )
        
        # Broadcast update via WebSocket
        await broadcast_checkin_update(follow_up, db)
        
        # Determine if escalation is needed based on response
        await evaluate_checkin_response(follow_up, db)
        
        return follow_up
        
    except Exception as e:
        logger.error(f"Failed to process check-in for follow-up {follow_up_id}: {str(e)}")
        raise


async def queue_followup_notification(
    follow_up: FollowUp,
    db: Session
) -> None:
    """
    Queue a notification to be sent at the scheduled follow-up time.
    
    In production, this would integrate with Celery, RQ, or similar task queue.
    For now, we simulate with immediate notification for demo purposes.
    """
    try:
        # In production, schedule with Celery:
        # from celery_app import send_followup_notification_task
        # send_followup_notification_task.apply_async(
        #     args=[follow_up.id],
        #     eta=follow_up.scheduled_time
        # )
        
        logger.info(
            f"Follow-up notification queued for follow-up {follow_up.id} "
            f"at {follow_up.scheduled_time}"
        )
        
        # For demo: send immediate notification
        if follow_up.user and follow_up.user.email:
            await NotificationService.send_followup_notification(follow_up, db)
        
    except Exception as e:
        logger.error(f"Failed to queue follow-up notification: {str(e)}")


async def broadcast_checkin_update(
    follow_up: FollowUp,
    db: Session
) -> None:
    """
    Broadcast follow-up check-in update via WebSocket to agencies.
    """
    try:
        report = follow_up.emergency_report
        if not report or not report.user:
            return
        
        user = report.user
        if not user.agency_id:
            return
        
        payload = {
            "type": "followup_checkin",
            "follow_up_id": follow_up.id,
            "report_id": report.id,
            "user_id": follow_up.user_id,
            "status": follow_up.status,
            "response": follow_up.user_response,
            "completed_at": follow_up.completed_at.isoformat() if follow_up.completed_at else None
        }
        
        await manager.broadcast_to_agency(user.agency_id, payload)
        logger.info(f"Follow-up check-in broadcasted for report {report.id}")
        
    except Exception as e:
        logger.error(f"WebSocket broadcast failed for follow-up: {str(e)}")


async def evaluate_checkin_response(
    follow_up: FollowUp,
    db: Session
) -> None:
    """
    Evaluate the check-in response and determine if escalation is needed.
    """
    try:
        report = follow_up.emergency_report
        if not report:
            return
        
        # Keywords indicating distress or continued crisis
        distress_keywords = [
            "worse", "harm", "suicide", "emergency", "crisis",
            "danger", "urgent", "help", "dying", "dying"
        ]
        
        response_lower = follow_up.user_response.lower() if follow_up.user_response else ""
        
        # Check if response indicates continued crisis
        if any(keyword in response_lower for keyword in distress_keywords):
            # Escalate report
            report.status = "ESCALATED"
            report.severity = "CRITICAL"
            db.commit()
            
            logger.warning(
                f"Follow-up response indicates crisis for report {report.id}. "
                f"Escalating. Response: {follow_up.user_response}"
            )
            
            # Send escalation alert to agencies
            await broadcast_escalation_alert(report, follow_up, db)
        else:
            # Update report as improved
            if report.status != "RESOLVED":
                report.status = "STABLE"
                db.commit()
                
                logger.info(f"Report {report.id} marked as stable based on check-in response")
        
    except Exception as e:
        logger.error(f"Error evaluating check-in response: {str(e)}")


async def broadcast_escalation_alert(
    report: EmergencyReport,
    follow_up: FollowUp,
    db: Session
) -> None:
    """
    Broadcast escalation alert when follow-up indicates continued crisis.
    """
    try:
        if not report.user or not report.user.agency_id:
            return
        
        alert_payload = {
            "type": "escalation_alert",
            "report_id": report.id,
            "follow_up_id": follow_up.id,
            "severity": "CRITICAL",
            "reason": "Continued crisis indicated in follow-up check-in",
            "user_response": follow_up.user_response,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await manager.broadcast_to_agency(report.user.agency_id, alert_payload)
        logger.info(f"Escalation alert broadcasted for report {report.id}")
        
    except Exception as e:
        logger.error(f"Failed to broadcast escalation alert: {str(e)}")


async def get_pending_followups_for_user(
    user_id: int,
    db: Session
) -> list:
    """
    Get all pending follow-ups for a user.
    """
    try:
        follow_ups = db.query(FollowUp).filter(
            FollowUp.user_id == user_id,
            FollowUp.status == "PENDING",
            FollowUp.scheduled_time <= datetime.utcnow()
        ).order_by(FollowUp.scheduled_time.desc()).all()
        
        return follow_ups
        
    except Exception as e:
        logger.error(f"Error retrieving pending follow-ups for user {user_id}: {str(e)}")
        raise
