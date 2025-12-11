from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LogBase(BaseModel):
    action: str = Field(..., min_length=1, max_length=100)
    notes: Optional[str] = Field(None, max_length=1000)

class LogCreate(LogBase):
    report_id: int = Field(..., gt=0)
    responder_id: Optional[int] = Field(None, gt=0)

class LogResponse(LogBase):
    id: int
    report_id: int
    responder_id: Optional[int] = None
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class LogListResponse(BaseModel):
    id: int
    report_id: int
    action: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
