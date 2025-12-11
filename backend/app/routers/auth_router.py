from typing import Any, Dict

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token as google_id_token
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db import get_db
from app.models.user import User
from app.schemas.user_schema import UserOut, TokenResponse

AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
SCOPES = ["openid", "email", "profile"]

router = APIRouter(prefix="/api/auth/google", tags=["auth"])


class GoogleCredentialPayload(BaseModel):
    token: str


def _ensure_client_configured() -> None:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_REDIRECT_URI:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth client configuration is incomplete.",
        )


def _build_authorization_url() -> str:
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


def _exchange_code_for_tokens(code: str) -> Dict[str, Any]:
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to exchange authorization code: {exc}",
        ) from exc

    tokens = response.json()
    if "id_token" not in tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google token exchange did not return an id_token.",
        )
    return tokens


def _verify_id_token(id_token: str) -> Dict[str, Any]:
    if not id_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Google ID token.",
        )

    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google client configuration is missing.",
        )

    try:
        return google_id_token.verify_oauth2_token(
            id_token,
            GoogleRequest(),
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google ID token: {exc}",
        ) from exc


def _upsert_user(db: Session, payload: Dict[str, Any]) -> User:
    email = payload.get("email")
    google_sub = payload.get("sub")
    if not email or not google_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google profile is missing required identifiers.",
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        user = User(
            email=email,
            name=payload.get("name"),
            picture=payload.get("picture"),
            google_id=google_sub,
            is_verified=True,
        )
        db.add(user)
    else:
        user.name = payload.get("name") or user.name
        user.picture = payload.get("picture") or user.picture
        if not user.google_id:
            user.google_id = google_sub
        user.is_verified = True

    db.commit()
    db.refresh(user)
    return user


def _build_token_response(user: User) -> TokenResponse:
    access_token = create_access_token({"sub": user.email})
    user_schema = UserOut.model_validate(user)
    return TokenResponse(
        access_token=access_token,
        user=user_schema,
    )


@router.get("/login", status_code=status.HTTP_307_TEMPORARY_REDIRECT, response_class=RedirectResponse)
async def google_login() -> RedirectResponse:
    _ensure_client_configured()
    return RedirectResponse(url=_build_authorization_url())


@router.get("/callback", response_model=TokenResponse)
async def google_callback(code: str, db: Session = Depends(get_db)) -> TokenResponse:
    _ensure_client_configured()
    tokens = _exchange_code_for_tokens(code)
    id_info = _verify_id_token(tokens.get("id_token"))
    user = _upsert_user(db, id_info)
    return _build_token_response(user)


@router.post("/verify", response_model=TokenResponse)
async def verify_google_token(
    payload: GoogleCredentialPayload, db: Session = Depends(get_db)
) -> TokenResponse:
    id_info = _verify_id_token(payload.token)
    user = _upsert_user(db, id_info)
    return _build_token_response(user)
