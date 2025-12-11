from sqlalchemy.orm import Session
import logging
from app.models.report import Report
from app.schemas.report_schema import ReportCreate, ReportUpdate

logger = logging.getLogger(__name__)

class ReportCRUD:
    @staticmethod
    def create(db: Session, report_in: ReportCreate, user_id: int) -> Report:
        """Create new report."""
        try:
            report = Report(
                user_id=user_id,
                text=report_in.text.strip(),
                location=report_in.location,
                latitude=report_in.latitude,
                longitude=report_in.longitude,
                category=getattr(report_in, 'category', None),
                is_critical=False,
                status="pending"
            )
            db.add(report)
            db.commit()
            db.refresh(report)
            logger.info(f"Report created: {report.id} by user {user_id}")
            return report
        except Exception as e:
            db.rollback()
            logger.error(f"Create report error: {str(e)}")
            raise
    
    @staticmethod
    def get(db: Session, report_id: int) -> Report:
        """Get report by ID."""
        try:
            return db.query(Report).filter(Report.id == report_id).first()
        except Exception as e:
            logger.error(f"Get report error: {str(e)}")
            return None
    
    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List all reports."""
        try:
            return db.query(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List reports error: {str(e)}")
            return []
    
    @staticmethod
    def list_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list:
        """List reports by user."""
        try:
            return db.query(Report).filter(Report.user_id == user_id).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List user reports error: {str(e)}")
            return []
    
    @staticmethod
    def list_by_status(db: Session, status: str, skip: int = 0, limit: int = 10) -> list:
        """List reports by status."""
        try:
            return db.query(Report).filter(Report.status == status).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List reports by status error: {str(e)}")
            return []
    
    @staticmethod
    def list_critical(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List critical reports."""
        try:
            return db.query(Report).filter(Report.is_critical == True).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List critical reports error: {str(e)}")
            return []
    
    @staticmethod
    def update(db: Session, report_id: int, report_update: ReportUpdate) -> Report:
        """Update report."""
        try:
            report = db.query(Report).filter(Report.id == report_id).first()
            if report:
                update_data = report_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    if value is not None:
                        setattr(report, field, value)
                db.commit()
                db.refresh(report)
                logger.info(f"Report updated: {report_id}")
            return report
        except Exception as e:
            db.rollback()
            logger.error(f"Update report error: {str(e)}")
            raise
    
    @staticmethod
    def delete(db: Session, report_id: int) -> bool:
        """Delete report."""
        try:
            report = db.query(Report).filter(Report.id == report_id).first()
            if report:
                db.delete(report)
                db.commit()
                logger.info(f"Report deleted: {report_id}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Delete report error: {str(e)}")
            raise
