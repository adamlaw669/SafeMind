import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.log import Log
from app.crud import log_crud

logger = logging.getLogger(__name__)


async def log_action(
    agent_id: int,
    action: str,
    target_id: int,
    db: Session,
    details: dict = None
) -> Log:
    """
    Log an action performed by an agent.
    
    Args:
        agent_id: ID of the user/agent performing the action
        action: Type of action performed (e.g., "STATUS_UPDATE", "REPORT_HANDLED", "ESCALATED")
        target_id: ID of the target resource (e.g., report ID)
        db: Database session
        details: Optional dictionary with additional details
    
    Returns:
        Log object created in database
    """
    try:
        log_entry = log_crud.create_log(
            db=db,
            agent_id=agent_id,
            action=action,
            target_id=target_id,
            details=details or {},
            timestamp=datetime.utcnow()
        )
        
        logger.info(
            f"Action logged: agent={agent_id}, action={action}, target={target_id}, "
            f"timestamp={log_entry.timestamp}"
        )
        
        return log_entry
        
    except Exception as e:
        logger.error(f"Failed to log action: {str(e)}")
        raise


async def log_status_change(
    agent_id: int,
    report_id: int,
    old_status: str,
    new_status: str,
    db: Session
) -> Log:
    """
    Log a status change on an emergency report.
    """
    details = {
        "old_status": old_status,
        "new_status": new_status,
        "changed_at": datetime.utcnow().isoformat()
    }
    
    return await log_action(
        agent_id=agent_id,
        action="STATUS_UPDATE",
        target_id=report_id,
        db=db,
        details=details
    )


async def log_report_response(
    agent_id: int,
    report_id: int,
    response_type: str,
    notes: str = None,
    db: Session = None
) -> Log:
    """
    Log an agency response to a report (handled, escalated, etc).
    """
    details = {
        "response_type": response_type,
        "notes": notes,
        "responded_at": datetime.utcnow().isoformat()
    }
    
    return await log_action(
        agent_id=agent_id,
        action="REPORT_RESPONSE",
        target_id=report_id,
        db=db,
        details=details
    )
