from sqlalchemy.orm import Session

from app.models.emergency import EmergencyReport
from app.schemas.emergency_schema import EmergencyReportCreate


def create_emergency_report(db: Session, data: EmergencyReportCreate) -> EmergencyReport:
    report = EmergencyReport(
        user_id=data.user_id,
        title=data.title,
        description=data.description,
        location=data.location,
        is_critical=True,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_report(db: Session, report_id: int) -> EmergencyReport | None:
    return db.query(EmergencyReport).filter(EmergencyReport.id == report_id).first()


def get_reports_by_user(db: Session, user_id: int):
    return (
        db.query(EmergencyReport)
        .filter(EmergencyReport.user_id == user_id)
        .order_by(EmergencyReport.created_at.desc())
        .all()
    )


def list_all_emergencies(db: Session):
    return db.query(EmergencyReport).order_by(EmergencyReport.created_at.desc()).all()
