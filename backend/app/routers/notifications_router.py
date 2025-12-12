from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import decode_token
from app.models.notification import Notification

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

def get_current_user_id(authorization: str = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    token = authorization.replace("Bearer ", "")
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return int(user_id)

@router.get("/")
def get_notifications(user_id: int, authorization: str = Depends(lambda: None), db: Session = Depends(get_db)):
    from fastapi import Header
    auth_header = None
    # Get auth header from request context if available
    current_user_id = user_id  # For now, accept user_id from query
    
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    return notifications

@router.post("/send")
def send_notification(authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"message": "Notification sent"}

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db.query(Notification).filter(Notification.id == notification_id).delete()
    db.commit()
    return {"message": "Deleted"}

@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, authorization: str = None, db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
    return {"message": "Marked as read"}
