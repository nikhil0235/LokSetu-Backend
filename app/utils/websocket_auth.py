from fastapi import WebSocket, HTTPException, status
from jose import JWTError, jwt
from app.data.postgres_adapter import PostgresAdapter
from typing import Optional
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def authenticate_websocket(websocket: WebSocket) -> Optional[dict]:
    """Authenticate WebSocket connection using token from query params or headers"""
    try:
        # Try to get token from query parameters first
        token = websocket.query_params.get("token")
        
        # If not in query params, try headers
        if not token:
            token = websocket.headers.get("authorization")
            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]
        
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token")
            return None
        
        # Decode JWT token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
                return None
        except JWTError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
            return None
        
        # Get user from database
        adapter = PostgresAdapter()
        user = adapter.get_user_by_username(username)
        if not user or not user.get('is_active'):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User not found or inactive")
            return None
        
        return user
        
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Authentication error")
        return None

def get_subordinate_user_ids(user: dict) -> list:
    """Get list of user IDs that the authenticated user can monitor"""
    adapter = PostgresAdapter()
    
    if user['role'] == 'super_admin':
        # Super admin can see all users
        users = adapter.get_users()
        return [u['user_id'] for u in users if u['is_active']]
    elif user['role'] == 'admin':
        # Admin can see users they created
        users = adapter.get_users()
        return [u['user_id'] for u in users if u['created_by'] == user['user_id'] and u['is_active']]
    else:
        # Booth boys and candidates can't monitor others
        return []