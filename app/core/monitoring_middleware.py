import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.api_monitoring_service import APIMonitoringService

class APIMonitoringMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.monitoring_service = APIMonitoringService()

    async def dispatch(self, request: Request, call_next):
        # Skip monitoring for health checks and static files
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        start_time = time.time()
        
        # Get user info if available
        user_id = None
        try:
            # Try to get user from request state (set by auth middleware)
            user_id = getattr(request.state, 'user_id', None)
        except:
            pass

        # Process request
        response = await call_next(request)
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Get client info
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent", "")[:500]  # Limit length
        
        # Log the request (non-blocking)
        try:
            self.monitoring_service.log_api_request(
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception:
            # Don't let monitoring failures affect the response
            pass
        
        return response