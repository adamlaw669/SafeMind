from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmergencyReportBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    location: Optional[str] = None

class EmergencyReportCreate(EmergencyReportBase):
    user_id: int

class EmergencyReportResponse(EmergencyReportBase):
    id: int
    user_id: int
    is_critical: bool
    risk_level: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
