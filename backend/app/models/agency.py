from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base import Base

class Agency(Base):
    __tablename__ = "agencies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
