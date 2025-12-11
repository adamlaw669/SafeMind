import logging
from app.core.config import settings
from collections import deque

logger = logging.getLogger(__name__)

class MessageQueue:
    def __init__(self):
        self.channels = {
            "emergency": deque(maxlen=100),
            "escalation": deque(maxlen=100),
            "followup": deque(maxlen=100)
        }
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize message queue."""
        try:
            logger.info(f"Initializing message queue with RABBITMQ_URL: {settings.RABBITMQ_URL[:50]}...")
            self.is_initialized = True
            logger.info("Message queue channels initialized: emergency, escalation, followup")
        except Exception as e:
            logger.error(f"Failed to initialize message queue: {str(e)}")
            raise
    
    async def publish(self, channel: str, message: dict):
        """Publish message to channel."""
        try:
            if channel not in self.channels:
                logger.warning(f"Unknown channel: {channel}")
                return False
            
            self.channels[channel].append(message)
            logger.info(f"Message published to {channel}: {message.get('type', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            return False
    
    async def subscribe(self, channel: str):
        """Subscribe to channel."""
        try:
            if channel not in self.channels:
                logger.warning(f"Unknown channel: {channel}")
                return None
            
            logger.info(f"Subscribed to channel: {channel}")
            return list(self.channels[channel])
        except Exception as e:
            logger.error(f"Failed to subscribe to channel: {str(e)}")
            return None
    
    async def publish_emergency(self, report_id: int, data: dict):
        """Publish emergency message."""
        return await self.publish("emergency", {"report_id": report_id, "type": "emergency", **data})
    
    async def publish_escalation(self, report_id: int, reason: str):
        """Publish escalation message."""
        return await self.publish("escalation", {"report_id": report_id, "type": "escalation", "reason": reason})
    
    async def publish_followup(self, report_id: int, delay_minutes: int):
        """Publish follow-up message."""
        return await self.publish("followup", {"report_id": report_id, "type": "followup", "delay_minutes": delay_minutes})

message_queue = MessageQueue()
