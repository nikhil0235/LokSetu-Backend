from typing import Optional
from datetime import datetime

class UserLocation:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = None,
        latitude: float = None,
        longitude: float = None,
        accuracy: Optional[float] = None,
        created_at: Optional[datetime] = None,
        **kwargs
    ):
        self.id = id
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.accuracy = accuracy
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            latitude=float(data.get("latitude")) if data.get("latitude") else None,
            longitude=float(data.get("longitude")) if data.get("longitude") else None,
            accuracy=float(data.get("accuracy")) if data.get("accuracy") else None,
            created_at=data.get("created_at")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }