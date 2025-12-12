from fastapi import Depends, HTTPException, status
# FIXED: Changed HTTPAuthCredentials -> HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.user import User
from app.core.security import decode_token

# Initialize the security scheme
security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security), # FIXED TYPE HINT
    db: Session = Depends(get_db)
) -> User:
    """
    Validates the Bearer token and returns the current user.
    """
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
        
    # Check if user exists in DB
    # Note: If 'sub' is email in your JWT, filter by email. If ID, filter by ID.
    # Based on your previous code, 'sub' seemed to be email.
    user = db.query(User).filter(User.email == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
        
    return user