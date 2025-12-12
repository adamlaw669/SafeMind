from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    picture: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    google_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    picture: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserOut):
    access_token: str
    token_type: str = "bearer"

class UserListResponse(BaseModel):
    id: int
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
