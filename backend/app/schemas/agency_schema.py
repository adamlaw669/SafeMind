from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class AgencyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    contact_email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=500)

class AgencyCreate(AgencyBase):
    pass

class AgencyUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=500)

class AgencyResponse(AgencyBase):
    id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AgencyListResponse(BaseModel):
    id: int
    name: str
    contact_email: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class AgentActionResponse(BaseModel):
    message: str
    agency_id: int
    success: bool = True
