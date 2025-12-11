from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to the Emergency Report
    report_id = Column(Integer, ForeignKey("emergency_reports.id"), nullable=False)
    
    # Direct link to User (for easier queries/auth checks)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Scheduling
    scheduled_for = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Content
    notes = Column(Text, nullable=True)  # Message/Notes for the follow-up
    response = Column(Text, nullable=True) # User's response text

    # Status: "PENDING", "COMPLETED", "CANCELLED", "MISSED"
    status = Column(String(50), default="PENDING", index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    # Router accesses this via 'follow_up.emergency_report'
    emergency_report = relationship("EmergencyReport", back_populates="followups")
    user = relationship("User")