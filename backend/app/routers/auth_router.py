from typing import Any, Dict
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token as google_id_token
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, hash_password, verify_password
from app.db.base import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut, TokenResponse, UserResponse, UserLogin

# Standard Auth Router
# Note: We remove the 'prefix' here because main.py sets it to /api/auth
router = APIRouter()

# --- STANDARD EMAIL/PASSWORD AUTH ---

@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password),
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "picture": new_user.picture,
        "is_verified": new_user.is_verified,
        "is_active": new_user.is_active,
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout():
    """
    Logout (Invalidate token on client side).
    """
    return {"message": "Logged out successfully"}

@router.post("/verify-email")
def verify_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.is_active = True
    db.commit()
    return {"message": "Email verified successfully"}

# --- GOOGLE AUTH ---

AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
SCOPES = ["openid", "email", "profile"]

class GoogleCredentialPayload(BaseModel):
    token: str

@router.get("/google/login", response_class=RedirectResponse)
async def google_login():
    from urllib.parse import urlencode
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{AUTHORIZATION_ENDPOINT}?{urlencode(params)}"

@router.get("/google/callback", response_model=TokenResponse)
async def google_callback(code: str, db: Session = Depends(get_db)):
    # Exchange code for token
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    try:
        res = requests.post(TOKEN_ENDPOINT, data=payload)
        res.raise_for_status()
        tokens = res.json()
    except Exception as e:
         raise HTTPException(status_code=400, detail=f"Google Auth Error: {str(e)}")

    # Verify ID token
    try:
        id_info = google_id_token.verify_oauth2_token(
            tokens["id_token"], 
            GoogleRequest(), 
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token")

    # Upsert User
    email = id_info["email"]
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            name=id_info.get("name"),
            picture=id_info.get("picture"),
            google_id=id_info["sub"],
            is_verified=True,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate JWT
    access_token = create_access_token({"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": user
    }