from sqlalchemy.orm import Session
import logging
from app.models.log import Log
from app.schemas.log_schema import LogCreate

logger = logging.getLogger(__name__)

class LogCRUD:
    @staticmethod
    def create(db: Session, log_in: LogCreate) -> Log:
        """Create new log entry."""
        try:
            log = Log(
                report_id=log_in.report_id,
                responder_id=log_in.responder_id,
                action=log_in.action.strip(),
                notes=log_in.notes.strip() if log_in.notes else None
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            logger.info(f"Log created: {log.id} for report {log_in.report_id}")
            return log
        except Exception as e:
            db.rollback()
            logger.error(f"Create log error: {str(e)}")
            raise
    
    @staticmethod
    def get(db: Session, log_id: int) -> Log:
        """Get log by ID."""
        try:
            return db.query(Log).filter(Log.id == log_id).first()
        except Exception as e:
            logger.error(f"Get log error: {str(e)}")
            return None
    
    @staticmethod
    def list_by_report(db: Session, report_id: int, skip: int = 0, limit: int = 10) -> list:
        """List logs for a report."""
        try:
            return db.query(Log).filter(Log.report_id == report_id).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List logs by report error: {str(e)}")
            return []
    
    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List all logs."""
        try:
            return db.query(Log).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List logs error: {str(e)}")
            return []
