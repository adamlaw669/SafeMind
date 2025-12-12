from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("emergency_reports.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    status = Column(String(50), default="PENDING", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    # FIXED: Name matches what EmergencyReport expects
    emergency_report = relationship("EmergencyReport", back_populates="followups")
    user = relationship("User")