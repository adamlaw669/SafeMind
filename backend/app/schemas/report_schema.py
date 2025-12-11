from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    location: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    category: Optional[str] = Field(None, max_length=100)

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=5000)
    status: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=500)
    is_critical: Optional[bool] = None

class ReportResponse(ReportBase):
    id: int
    user_id: int
    is_critical: bool
    status: str
    timestamp: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReportListResponse(BaseModel):
    id: int
    user_id: int
    text: str = Field(..., max_length=500)
    is_critical: bool
    status: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class EmergencyReportCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    location: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
