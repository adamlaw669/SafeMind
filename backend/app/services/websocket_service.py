from typing import Dict, Set
from fastapi import WebSocket
import logging
import json

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.agency_subscriptions: Dict[int, Set[str]] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        """Accept WebSocket connection and register user."""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected via WebSocket")
    
    async def disconnect(self, user_id: str, websocket: WebSocket):
        """Remove WebSocket connection."""
        try:
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from WebSocket")
        except Exception as e:
            logger.error(f"Disconnect error for {user_id}: {str(e)}")
    
    async def subscribe_agency(self, agency_id: int, user_id: str):
        """Subscribe user to agency alerts."""
        try:
            if agency_id <= 0 or not user_id:
                logger.warning(f"Invalid subscription: agency_id={agency_id}, user_id={user_id}")
                return
            
            if agency_id not in self.agency_subscriptions:
                self.agency_subscriptions[agency_id] = set()
            self.agency_subscriptions[agency_id].add(user_id)
            logger.info(f"Agency {agency_id} subscribed via user {user_id}")
        except Exception as e:
            logger.error(f"Subscribe agency error: {str(e)}")
    
    async def unsubscribe_agency(self, agency_id: int, user_id: str):
        """Unsubscribe user from agency alerts."""
        try:
            if agency_id in self.agency_subscriptions:
                self.agency_subscriptions[agency_id].discard(user_id)
            logger.info(f"User {user_id} unsubscribed from agency {agency_id}")
        except Exception as e:
            logger.error(f"Unsubscribe agency error: {str(e)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected users."""
        if not message or not isinstance(message, dict):
            logger.warning("Invalid broadcast message")
            return
        
        disconnected = []
        for user_id, connections in list(self.active_connections.items()):
            for websocket in list(connections):
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to broadcast to {user_id}: {str(e)}")
                    disconnected.append((user_id, websocket))
        
        for user_id, websocket in disconnected:
            await self.disconnect(user_id, websocket)
    
    async def broadcast_to_agency(self, agency_id: int, message: dict):
        """Broadcast message to users subscribed to agency."""
        if agency_id <= 0 or not message or not isinstance(message, dict):
            logger.warning(f"Invalid agency broadcast: agency_id={agency_id}")
            return
        
        if agency_id in self.agency_subscriptions:
            disconnected = []
            for user_id in list(self.agency_subscriptions[agency_id]):
                if user_id in self.active_connections:
                    for websocket in list(self.active_connections[user_id]):
                        try:
                            await websocket.send_json(message)
                        except Exception as e:
                            logger.error(f"Failed to send to agency {agency_id}: {str(e)}")
                            disconnected.append((user_id, websocket))
            
            for user_id, websocket in disconnected:
                await self.disconnect(user_id, websocket)
    
    async def send_to_user(self, user_id: str, message: dict):
        """Send message to specific user."""
        if not user_id or not message or not isinstance(message, dict):
            logger.warning(f"Invalid user send: user_id={user_id}")
            return
        
        if user_id in self.active_connections:
            disconnected = []
            for websocket in list(self.active_connections[user_id]):
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send to user {user_id}: {str(e)}")
                    disconnected.append(websocket)
            
            for websocket in disconnected:
                await self.disconnect(user_id, websocket)

manager = ConnectionManager()
