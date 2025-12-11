from typing import Optional, Dict, Any
from fastapi import WebSocket
from app.services.websocket_service import manager


class NotificationService:
    """
    Centralized notification manager.
    Provides:
    - email notifications (stub)
    - SMS notifications (stub)
    - push notifications (stub)
    - websocket emergency alert broadcasts
    """

    @staticmethod
    def send_email_notification(to: str, subject: str, message: str) -> None:
        # TODO: integrate real SMTP or SendGrid
        print(f"[EMAIL] To: {to} | Subject: {subject} | Message: {message}")

    @staticmethod
    def send_sms_notification(phone: str, message: str) -> None:
        # TODO: integrate real SMS gateway
        print(f"[SMS] To: {phone} | Message: {message}")

    @staticmethod
    def send_push_notification(user_id: int, message: str) -> None:
        # TODO: integrate real push service
        print(f"[PUSH] User: {user_id} | Message: {message}")

    @staticmethod
    async def broadcast_websocket_alert(alert: Dict[str, Any]) -> None:
        """
        Sends real-time alerts to all connected agencies.
        """
        await websocket_manager.broadcast(alert)

    @staticmethod
    async def send_alert(
        user_email: Optional[str],
        user_phone: Optional[str],
        websocket_payload: Dict[str, Any]
    ) -> None:
        """
        High-level helper combining:
        - email
        - sms
        - websocket notification
        """

        subject = "SafeMind Emergency Alert"
        message = f"Emergency detected: {websocket_payload}"

        if user_email:
            NotificationService.send_email_notification(user_email, subject, message)

        if user_phone:
            NotificationService.send_sms_notification(user_phone, message)

        await NotificationService.broadcast_websocket_alert(websocket_payload)
