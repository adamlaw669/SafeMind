from sqlalchemy.orm import Session
from app.models.log import Log
from app.schemas.log_schema import LogCreate

def create_log(db: Session, data: LogCreate) -> Log:
    log = Log(
        action=data.action,
        description=data.description,
        user_id=data.user_id,
        agency_id=data.agency_id,
        severity=data.severity,
        source=data.source
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_log_by_id(db: Session, log_id: int) -> Log | None:
    return db.query(Log).filter(Log.id == log_id).first()


def list_logs(db: Session, limit: int = 100):
    return (
        db.query(Log)
        .order_by(Log.created_at.desc())
        .limit(limit)
        .all()
    )


def list_logs_for_agency(db: Session, agency_id: int, limit: int = 100):
    return (
        db.query(Log)
        .filter(Log.agency_id == agency_id)
        .order_by(Log.created_at.desc())
        .limit(limit)
        .all()
    )


def list_logs_for_user(db: Session, user_id: int, limit: int = 100):
    return (
        db.query(Log)
        .filter(Log.user_id == user_id)
        .order_by(Log.created_at.desc())
        .limit(limit)
        .all()
    )
