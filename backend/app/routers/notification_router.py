from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import logging
from app.db.base import get_db
from app.schemas.user_schema import UserOut
from app.core.security import get_current_user, decode_token
from app.services.websocket_service import manager

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def get_notifications(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for user."""
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    skip = max(0, skip)
    limit = min(100, max(1, limit))
    return {"notifications": [], "total": 0}

@router.post("/send")
async def send_notification(
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send notification."""
    return {"message": "Notification sent"}

@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    if notification_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid notification ID")
    return {"message": "Notification marked as read"}

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete notification."""
    if notification_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid notification ID")
    return {"message": "Notification deleted"}

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
