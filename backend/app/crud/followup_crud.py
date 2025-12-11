from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.followup import FollowUp
from app.schemas.followup_schema import FollowupRequest

def create_followup(
    db: Session, 
    report_id: int, 
    user_id: int, 
    scheduled_time: datetime, 
    notes: Optional[str] = None
) -> FollowUp:
    db_obj = FollowUp(
        report_id=report_id,
        user_id=user_id,
        scheduled_for=scheduled_time,
        notes=notes,
        status="PENDING"
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_followup(db: Session, followup_id: int) -> Optional[FollowUp]:
    return db.query(FollowUp).filter(FollowUp.id == followup_id).first()

def get_followups_by_report(
    db: Session, 
    report_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[FollowUp]:
    return (
        db.query(FollowUp)
        .filter(FollowUp.report_id == report_id)
        .order_by(FollowUp.scheduled_for.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_pending_followups_for_user(
    db: Session, 
    user_id: int
) -> List[FollowUp]:
    return (
        db.query(FollowUp)
        .filter(
            FollowUp.user_id == user_id,
            FollowUp.status == "PENDING"
        )
        .order_by(FollowUp.scheduled_for.asc())
        .all()
    )