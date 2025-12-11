import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.emergency import EmergencyReport
from app.models.followup import FollowUp
from app.services.websocket_service import manager
from app.services.notification_service import NotificationService
from app.core.nlp_model import analyze_risk_level

logger = logging.getLogger(__name__)


async def process_emergency_report(
    report: EmergencyReport,
    db: Session
) -> None:
    """
    Process emergency report with NLP analysis, notifications, WebSocket broadcast, and follow-up scheduling.
    """
    try:
        # Step 1: NLP Risk Detection
        risk_score = await analyze_risk_level(report.description)
        report.risk_score = risk_score
        
        # Step 2: Determine severity and priority
        if risk_score >= 0.8:
            report.severity = "CRITICAL"
            priority = 1
        elif risk_score >= 0.6:
            report.severity = "HIGH"
            priority = 2
        else:
            report.severity = "MEDIUM"
            priority = 3
        
        db.commit()
        db.refresh(report)
        logger.info(f"Emergency report {report.id} analyzed with risk_score: {risk_score}")
        
        # Step 3: WebSocket Broadcast to relevant agencies
        await broadcast_emergency_alert(report, db)
        
        # Step 4: Send notifications to assigned agencies
        await NotificationService.send_emergency_notification(report, db)
        
        # Step 5: Schedule follow-up
        await schedule_follow_up(report, priority, db)
        
        logger.info(f"Emergency report {report.id} processed successfully")
        
    except Exception as e:
        logger.error(f"Error processing emergency report {report.id}: {str(e)}")
        raise


async def broadcast_emergency_alert(
    report: EmergencyReport,
    db: Session
) -> None:
    """
    Broadcast emergency alert via WebSocket to subscribed agencies.
    """
    try:
        # Get user's agency information
        user = report.user
        if not user or not user.agency_id:
            logger.warning(f"Emergency report {report.id} has no agency assignment")
            return
        
        alert_payload = {
            "type": "emergency_alert",
            "report_id": report.id,
            "severity": report.severity,
            "risk_score": report.risk_score,
            "location": report.location,
            "description": report.description,
            "user_name": user.name,
            "timestamp": report.created_at.isoformat()
        }
        
        await manager.broadcast_to_agency(user.agency_id, alert_payload)
        logger.info(f"Emergency alert broadcasted for report {report.id} to agency {user.agency_id}")
        
    except Exception as e:
        logger.error(f"WebSocket broadcast failed for report {report.id}: {str(e)}")


async def schedule_follow_up(
    report: EmergencyReport,
    priority: int,
    db: Session
) -> None:
    """
    Schedule automated follow-up based on severity and priority.
    """
    try:
        # Determine follow-up schedule based on priority
        follow_up_intervals = {
            1: 15,    # CRITICAL: 15 minutes
            2: 60,    # HIGH: 1 hour
            3: 240    # MEDIUM: 4 hours
        }
        
        minutes_until_followup = follow_up_intervals.get(priority, 240)
        scheduled_time = datetime.utcnow() + timedelta(minutes=minutes_until_followup)
        
        follow_up = FollowUp(
            emergency_report_id=report.id,
            user_id=report.user_id,
            status="PENDING",
            scheduled_time=scheduled_time,
            follow_up_type="AUTOMATED",
            notes=f"Automated follow-up for {report.severity} severity report"
        )
        
        db.add(follow_up)
        db.commit()
        db.refresh(follow_up)
        
        logger.info(f"Follow-up {follow_up.id} scheduled for report {report.id} at {scheduled_time}")
        
    except Exception as e:
        logger.error(f"Failed to schedule follow-up for report {report.id}: {str(e)}")
