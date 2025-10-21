from typing import Dict, Optional
from datetime import datetime, timedelta
import threading

class LocationCache:
    def __init__(self):
        self._cache: Dict[int, dict] = {}
        self._lock = threading.Lock()
        self.ONLINE_THRESHOLD_MINUTES = 2

    def update_location(self, user_id: int, latitude: float, longitude: float, accuracy: Optional[float] = None):
        """Update user's latest location in cache"""
        with self._lock:
            self._cache[user_id] = {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
                "last_updated": datetime.now(),
                "is_online": True
            }

    def get_location(self, user_id: int) -> Optional[dict]:
        """Get user's latest location from cache"""
        with self._lock:
            location = self._cache.get(user_id)
            if location:
                # Check if user is still online
                time_diff = datetime.now() - location["last_updated"]
                location["is_online"] = time_diff.total_seconds() < (self.ONLINE_THRESHOLD_MINUTES * 60)
            return location

    def get_all_locations(self) -> Dict[int, dict]:
        """Get all cached locations"""
        with self._lock:
            current_time = datetime.now()
            result = {}
            for user_id, location in self._cache.items():
                time_diff = current_time - location["last_updated"]
                location_copy = location.copy()
                location_copy["is_online"] = time_diff.total_seconds() < (self.ONLINE_THRESHOLD_MINUTES * 60)
                result[user_id] = location_copy
            return result

    def remove_user(self, user_id: int):
        """Remove user from cache"""
        with self._lock:
            self._cache.pop(user_id, None)

    def cleanup_offline_users(self, hours: int = 24):
        """Remove users who haven't updated location in specified hours"""
        with self._lock:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=hours)
            
            offline_users = [
                user_id for user_id, location in self._cache.items()
                if location["last_updated"] < cutoff_time
            ]
            
            for user_id in offline_users:
                del self._cache[user_id]
            
            return len(offline_users)

# Global cache instance
location_cache = LocationCache()