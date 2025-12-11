from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FollowupRequest(BaseModel):
    hours: int = Field(..., gt=0, le=720, description="Hours until follow-up (1-720)")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")

class FollowupCheckinRequest(BaseModel):
    followup_id: int = Field(..., gt=0, description="Follow-up ID")
    response: str = Field(..., min_length=1, max_length=1000, description="Check-in response")

class FollowupResponse(BaseModel):
    id: int
    emergency_report_id: int
    user_id: int
    status: str
    follow_up_type: str
    scheduled_time: datetime
    completed_at: Optional[datetime] = None
    user_response: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FollowupListResponse(BaseModel):
    id: int
    emergency_report_id: int
    status: str
    scheduled_time: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
