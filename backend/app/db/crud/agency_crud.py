from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from app.models.agency import Agency
from app.schemas.agency_schema import AgencyCreate, AgencyUpdate

logger = logging.getLogger(__name__)

class AgencyCRUD:
    @staticmethod
    def create(db: Session, agency_in: AgencyCreate) -> Agency:
        """Create new agency."""
        try:
            agency = Agency(
                name=agency_in.name.strip(),
                contact_email=agency_in.contact_email.lower(),
                phone=agency_in.phone,
                location=agency_in.location,
                is_verified=False,
                is_active=True
            )
            db.add(agency)
            db.commit()
            db.refresh(agency)
            logger.info(f"Agency created: {agency.id}")
            return agency
        except IntegrityError:
            db.rollback()
            logger.error(f"Agency already exists: {agency_in.contact_email}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Create agency error: {str(e)}")
            raise
    
    @staticmethod
    def get(db: Session, agency_id: int) -> Agency:
        """Get agency by ID."""
        try:
            return db.query(Agency).filter(Agency.id == agency_id).first()
        except Exception as e:
            logger.error(f"Get agency error: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Agency:
        """Get agency by email."""
        try:
            return db.query(Agency).filter(Agency.contact_email == email.lower()).first()
        except Exception as e:
            logger.error(f"Get agency by email error: {str(e)}")
            return None
    
    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List all agencies."""
        try:
            return db.query(Agency).order_by(Agency.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List agencies error: {str(e)}")
            return []
    
    @staticmethod
    def list_verified(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List verified agencies."""
        try:
            return db.query(Agency).filter(Agency.is_verified == True).order_by(Agency.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List verified agencies error: {str(e)}")
            return []
    
    @staticmethod
    def update(db: Session, agency_id: int, agency_update: AgencyUpdate) -> Agency:
        """Update agency."""
        try:
            agency = db.query(Agency).filter(Agency.id == agency_id).first()
            if agency:
                update_data = agency_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    if value is not None:
                        setattr(agency, field, value)
                db.commit()
                db.refresh(agency)
                logger.info(f"Agency updated: {agency_id}")
            return agency
        except Exception as e:
            db.rollback()
            logger.error(f"Update agency error: {str(e)}")
            raise
    
    @staticmethod
    def delete(db: Session, agency_id: int) -> bool:
        """Delete agency."""
        try:
            agency = db.query(Agency).filter(Agency.id == agency_id).first()
            if agency:
                db.delete(agency)
                db.commit()
                logger.info(f"Agency deleted: {agency_id}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Delete agency error: {str(e)}")
            raise
