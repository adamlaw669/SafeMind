from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Generic Log Fields
    action = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # Mapped from 'notes' in your old version
    severity = Column(String(50), nullable=True)  # e.g., "info", "warning", "critical"
    source = Column(String(100), nullable=True)   # e.g., "agency_dashboard", "system"

    # Foreign Keys (Nullable because a log might be general system info)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("emergency_reports.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    agency = relationship("Agency")
    # Note: Ensure "EmergencyReport" model has the back-reference if needed, 
    # or you can leave the relationship one-way for logs.