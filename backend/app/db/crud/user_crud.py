from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password

logger = logging.getLogger(__name__)

class UserCRUD:
    @staticmethod
    def create(db: Session, user_in: UserCreate) -> User:
        """Create new user."""
        try:
            password_hash = hash_password(user_in.password) if user_in.password else None
            user = User(
                email=user_in.email,
                name=user_in.name,
                picture=user_in.picture,
                google_id=user_in.google_id,
                password_hash=password_hash,
                is_verified=False,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User created: {user.email}")
            return user
        except IntegrityError:
            db.rollback()
            logger.error(f"User already exists: {user_in.email}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Create user error: {str(e)}")
            raise
    
    @staticmethod
    def get(db: Session, user_id: int) -> User:
        """Get user by ID."""
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        """Get user by email."""
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Get user by email error: {str(e)}")
            return None
    
    @staticmethod
    def get_by_google_id(db: Session, google_id: str) -> User:
        """Get user by Google ID."""
        try:
            return db.query(User).filter(User.google_id == google_id).first()
        except Exception as e:
            logger.error(f"Get user by google_id error: {str(e)}")
            return None
    
    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        """List all users."""
        try:
            return db.query(User).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"List users error: {str(e)}")
            return []
    
    @staticmethod
    def update(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """Update user."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                update_data = user_update.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    if value is not None:
                        setattr(user, field, value)
                db.commit()
                db.refresh(user)
                logger.info(f"User updated: {user_id}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Update user error: {str(e)}")
            raise
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete user."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
                db.commit()
                logger.info(f"User deleted: {user_id}")
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Delete user error: {str(e)}")
            raise
