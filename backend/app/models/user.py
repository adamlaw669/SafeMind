from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    
    # FIXED: Added missing picture column
    picture = Column(String, nullable=True) 
    
    # FIXED: Renamed to match what tests are likely using, OR keep as hashed_password
    # Let's standardize on 'hashed_password' as it's more common, but check your Auth Router.
    # Your auth router uses: hashed_password=hash_password(user_data.password)
    # Your tests use: password_hash=hash_password("password123")
    # WE MUST PICK ONE. Let's pick 'hashed_password' and fix the tests.
    hashed_password = Column(String)
    
    google_id = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    emergency_reports = relationship("EmergencyReport", back_populates="user")
    followups = relationship("FollowUp", back_populates="user")