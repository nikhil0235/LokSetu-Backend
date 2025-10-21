from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from app.services.api_monitoring_service import APIMonitoringService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/api-stats")
async def get_api_stats(
    hours: int = Query(24, description="Hours to look back"),
    user: User = Depends(get_current_user)
):
    """Get API usage statistics"""
    if user['role'] not in ['super_admin', 'admin']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    stats = APIMonitoringService.get_api_stats(hours)
    return {
        "period_hours": hours,
        "stats": stats
    }

@router.get("/error-rates")
async def get_error_rates(
    hours: int = Query(24, description="Hours to look back"),
    user: User = Depends(get_current_user)
):
    """Get error rates by endpoint"""
    if user['role'] not in ['super_admin', 'admin']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    error_rates = APIMonitoringService.get_error_rates(hours)
    return {
        "period_hours": hours,
        "error_rates": error_rates
    }

@router.get("/system-health")
async def get_system_health():
    """Basic system health check"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.post("/cleanup")
async def manual_cleanup(
    user: User = Depends(get_current_user)
):
    """Manually trigger cleanup of old data"""
    if user['role'] != 'super_admin':
        raise HTTPException(status_code=403, detail="Access denied")
    
    from app.services.cleanup_scheduler import cleanup_scheduler
    result = cleanup_scheduler.run_manual_cleanup()
    return result