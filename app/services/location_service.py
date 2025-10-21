from typing import List, Optional, Dict
from datetime import datetime, timedelta
from app.data.connection import get_db_connection
from app.models.location import UserLocation
from app.services.location_cache import location_cache
from app.utils.logger import logger

class LocationService:
    def __init__(self):
        self.cache = location_cache

    def update_user_location(self, user_id: int, latitude: float, longitude: float, accuracy: Optional[float] = None):
        """Update user location in both database and cache"""
        # Store in database for history
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_locations (user_id, latitude, longitude, accuracy) VALUES (%s, %s, %s, %s)",
                (user_id, latitude, longitude, accuracy)
            )
            conn.commit()

        # Update cache for real-time access
        self.cache.update_location(user_id, latitude, longitude, accuracy)
        logger.info(f"Updated location for user {user_id}")

    def get_user_latest_location(self, user_id: int) -> Optional[dict]:
        """Get user's latest location from cache"""
        return self.cache.get_location(user_id)

    def get_user_location_history(self, user_id: int, hours: int = 24) -> List[UserLocation]:
        """Get user's location history from database"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, latitude, longitude, accuracy, created_at 
                FROM user_locations 
                WHERE user_id = %s AND created_at >= %s 
                ORDER BY created_at DESC
                """,
                (user_id, datetime.now() - timedelta(hours=hours))
            )
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            return [UserLocation.from_dict(dict(zip(columns, row))) for row in rows]

    def get_subordinate_locations(self, supervisor_user: dict) -> Dict[int, dict]:
        """Get locations of users under supervisor's hierarchy"""
        subordinate_ids = self._get_subordinate_user_ids(supervisor_user)
        
        all_locations = self.cache.get_all_locations()
       
        # Filter only subordinate locations
        return {
            user_id: location for user_id, location in all_locations.items()
            if user_id in subordinate_ids
        }

    def _get_subordinate_user_ids(self, supervisor_user: dict) -> List[int]:
        """Get list of user IDs that supervisor can monitor"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if supervisor_user['role'] == 'super_admin':
                # Super admin can see all users
                cursor.execute("SELECT user_id FROM users WHERE is_active = true")
            elif supervisor_user['role'] == 'admin':
                # Admin can see users they created
                cursor.execute("SELECT user_id FROM users WHERE created_by = %s AND is_active = true", 
                             (supervisor_user['user_id'],))
            else:
                # Booth boys and candidates can't monitor others
                return []
            
            return [row[0] for row in cursor.fetchall()]

    def get_user_info_with_location(self, user_ids: List[int]) -> List[dict]:
        """Get user info combined with their latest location"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            placeholders = ','.join(['%s'] * len(user_ids))
            cursor.execute(
                f"""
                SELECT user_id, username, full_name, role 
                FROM users 
                WHERE user_id IN ({placeholders}) AND is_active = true
                """,
                user_ids
            )
            columns = [desc[0] for desc in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Combine with location data
        result = []
        for user in users:
            location_data = self.cache.get_location(user['user_id'])
            
            # Format location data for API response
            formatted_location = None
            if location_data:
                formatted_location = {
                    'latitude': location_data['latitude'],
                    'longitude': location_data['longitude'],
                    'accuracy': location_data['accuracy'],
                    'last_updated': location_data['last_updated'],
                    'is_online': location_data['is_online']
                }
            
            result.append({
                **user,
                'latest_location': formatted_location,
                'is_online': location_data['is_online'] if location_data else False,
                'last_seen': location_data['last_updated'] if location_data else None
            })
        
        return result

    def cleanup_old_locations(self):
        """Clean up old location records (run as scheduled job)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM user_locations WHERE created_at < %s",
                (datetime.now() - timedelta(hours=24),)
            )
            deleted_count = cursor.rowcount
            conn.commit()
            
        # Also cleanup cache
        cache_cleaned = self.cache.cleanup_offline_users(24)
        
        logger.info(f"Cleaned up {deleted_count} old location records and {cache_cleaned} offline users from cache")