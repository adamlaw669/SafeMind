from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class EmergencyReport(Base):
    __tablename__ = "emergency_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    location = Column(String(255), nullable=True)
    is_critical = Column(Boolean, default=True)
    risk_level = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="emergency_reports")
    
    # FIXED: Added this relationship
    followups = relationship("FollowUp", back_populates="emergency_report", cascade="all, delete-orphan")
    
    # Optional: If you use logs
    # logs = relationship("LogEntry", back_populates="report")