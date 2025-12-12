from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import logging
from app.db.base import get_db
from app.models.user import User
from app.core.security import get_current_user, decode_token
from app.services.websocket_service import manager
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def get_notifications(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications."""
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' notifications"
        )
    
    from app.models.notification import Notification
    
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id
    ).all()
    
    return [
        {
            "id": n.id,
            "user_id": n.user_id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ]

@router.post("/send")
async def send_notification(
    user_id: int,
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a notification."""
    from app.models.notification import Notification
    
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at
    }

@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    from app.models.notification import Notification
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users' notifications"
        )
    
    notification.is_read = True
    db.commit()
    
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at
    }

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification."""
    from app.models.notification import Notification
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other users' notifications"
        )
    
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}

@router.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket, token: str):
    """WebSocket endpoint for real-time alerts."""
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logger.warning("WebSocket connection rejected: invalid token")
        return
    
    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        logger.warning("WebSocket connection rejected: no user_id")
        return
    
    await manager.connect(str(user_id), websocket)
    logger.info(f"WebSocket connected for user {user_id}")
    
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "subscribe_agency":
                agency_id = data.get("agency_id")
                if agency_id and agency_id > 0:
                    await manager.subscribe_agency(agency_id, str(user_id))
                    logger.info(f"User {user_id} subscribed to agency {agency_id}")
            elif data.get("type") == "unsubscribe_agency":
                agency_id = data.get("agency_id")
                if agency_id and agency_id > 0:
                    await manager.unsubscribe_agency(agency_id, str(user_id))
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        await manager.disconnect(str(user_id), websocket)
        logger.info(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
        await manager.disconnect(str(user_id), websocket)
