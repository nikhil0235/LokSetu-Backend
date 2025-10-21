from fastapi import APIRouter, Depends, HTTPException, WebSocket, Query
from fastapi.websockets import WebSocketDisconnect
from typing import List
from app.schemas.location_schema import LocationUpdate, UserLocationInfo, LocationHistoryResponse, CacheLocationResponse
from app.services.location_service import LocationService
from app.services.websocket_manager import websocket_manager
from app.api.deps import get_current_user
from app.models.user import User
from app.utils.websocket_auth import authenticate_websocket, get_subordinate_user_ids
from app.utils.logger import logger

router = APIRouter()

@router.post("/location")
async def update_my_location(
    location: LocationUpdate,
    user: User = Depends(get_current_user)
):
    """Update current user's location (called by mobile app every 30 seconds)"""
    location_service = LocationService()
    
    # Update location in database and cache
    location_service.update_user_location(
        user_id=user['user_id'],
        latitude=location.latitude,
        longitude=location.longitude,
        accuracy=location.accuracy
    )
    
    # Get updated location data for WebSocket broadcast
    location_data = location_service.get_user_latest_location(user['user_id'])
    
    # Broadcast to authorized supervisors via WebSocket
    await websocket_manager.broadcast_location_update(user['user_id'], location_data)
    
    return {"message": "Location updated successfully"}

@router.get("/locations", response_model=List[UserLocationInfo])
async def get_subordinate_locations(
    user: User = Depends(get_current_user)
):
    """Get locations of all subordinate users (REST API fallback)"""
    if user['role'] not in ['super_admin', 'admin']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    location_service = LocationService()
    
    # Get subordinate locations from cache
    subordinate_locations = location_service.get_subordinate_locations(user)
    
    if not subordinate_locations:
        return []
    
    # Get user info combined with locations
    user_ids = list(subordinate_locations.keys())
    users_with_locations = location_service.get_user_info_with_location(user_ids)
    
    return users_with_locations

@router.get("/locations/{user_id}/history", response_model=LocationHistoryResponse)
async def get_user_location_history(
    user_id: int,
    hours: int = Query(24, ge=1, le=168, description="Hours to look back (max 7 days)"),
    user: User = Depends(get_current_user)
):
    """Get location history for a specific user"""
    if user['role'] not in ['super_admin', 'admin']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    location_service = LocationService()
    
    # Check if user can access this subordinate
    subordinate_ids = location_service._get_subordinate_user_ids(user)
    if user_id not in subordinate_ids:
        raise HTTPException(status_code=403, detail="Access denied to this user's location")
    
    # Get location history
    locations = location_service.get_user_location_history(user_id, hours)
    
    return LocationHistoryResponse(
        user_id=user_id,
        locations=[loc.to_dict() for loc in locations],
        total_count=len(locations)
    )

@router.websocket("/ws/locations")
async def websocket_locations(websocket: WebSocket):
    """WebSocket endpoint for real-time location updates"""
    user = None
    try:
        # Authenticate WebSocket connection
        user = await authenticate_websocket(websocket)
        if not user:
            return  # Connection already closed by auth function
        
        # Check if user has permission to monitor locations
        if user['role'] not in ['super_admin', 'admin']:
            await websocket.close(code=1008, reason="Access denied")
            return
        
        # Get subordinate user IDs
        subordinate_ids = get_subordinate_user_ids(user)
        
        # Connect to WebSocket manager
        await websocket_manager.connect(websocket, user['user_id'], subordinate_ids)
        
        # Send initial locations
        location_service = LocationService()
        subordinate_locations = location_service.get_subordinate_locations(user)
        await websocket_manager.send_initial_locations(user['user_id'], subordinate_locations)
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Receive heartbeat or other messages
                message = await websocket.receive_text()
                # Handle ping/pong or other control messages if needed
                if message == "ping":
                    await websocket.send_text("pong")
            except WebSocketDisconnect:
                break
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Clean up connection
        if user:
            websocket_manager.disconnect(user['user_id'])