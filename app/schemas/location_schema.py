from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LocationUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    accuracy: Optional[float] = Field(None, ge=0, description="Accuracy in meters")

class LocationResponse(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    latitude: float
    longitude: float
    accuracy: Optional[float]
    created_at: Optional[datetime] = None

class CacheLocationResponse(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float]
    last_updated: datetime
    is_online: bool

class UserLocationInfo(BaseModel):
    user_id: int
    username: str
    full_name: Optional[str]
    role: str
    latest_location: Optional[CacheLocationResponse]
    is_online: bool
    last_seen: Optional[datetime]

class LocationHistoryResponse(BaseModel):
    user_id: int
    locations: List[LocationResponse]
    total_count: int