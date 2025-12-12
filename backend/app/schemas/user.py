from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
