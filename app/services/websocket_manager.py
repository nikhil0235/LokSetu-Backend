from typing import Dict, List
from fastapi import WebSocket
import json
import asyncio
from app.utils.logger import logger

class LocationWebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_permissions: Dict[int, List[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, subordinate_ids: List[int]):
        """Accept WebSocket connection and store user permissions"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_permissions[user_id] = subordinate_ids
        logger.info(f"WebSocket connected for user {user_id}")

    def disconnect(self, user_id: int):
        """Remove WebSocket connection"""
        self.active_connections.pop(user_id, None)
        self.user_permissions.pop(user_id, None)
        logger.info(f"WebSocket disconnected for user {user_id}")

    async def send_personal_message(self, message: dict, user_id: int):
        """Send message to specific user"""
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message to user {user_id}: {e}")
                self.disconnect(user_id)

    async def broadcast_location_update(self, updated_user_id: int, location_data: dict):
        """Broadcast location update to authorized supervisors"""
        message = {
            "type": "location_update",
            "user_id": updated_user_id,
            "data": location_data,
            "timestamp": location_data.get("last_updated").isoformat() if location_data.get("last_updated") else None
        }

        # Find all supervisors who can see this user
        authorized_supervisors = []
        for supervisor_id, subordinate_ids in self.user_permissions.items():
            if updated_user_id in subordinate_ids:
                authorized_supervisors.append(supervisor_id)

        # Send to all authorized supervisors
        for supervisor_id in authorized_supervisors:
            await self.send_personal_message(message, supervisor_id)

    async def send_initial_locations(self, user_id: int, locations_data: Dict[int, dict]):
        """Send initial location data when user connects"""
        message = {
            "type": "initial_locations",
            "data": locations_data
        }
        await self.send_personal_message(message, user_id)

    async def broadcast_user_status(self, user_id: int, is_online: bool):
        """Broadcast user online/offline status"""
        message = {
            "type": "user_status",
            "user_id": user_id,
            "is_online": is_online,
            "timestamp": None
        }

        # Find supervisors who can see this user
        for supervisor_id, subordinate_ids in self.user_permissions.items():
            if user_id in subordinate_ids:
                await self.send_personal_message(message, supervisor_id)

# Global WebSocket manager instance
websocket_manager = LocationWebSocketManager()