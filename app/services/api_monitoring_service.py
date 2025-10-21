import asyncio
from typing import Optional
from app.data.connection import get_db_connection
from app.utils.logger import logger

class APIMonitoringService:
    @staticmethod
    def log_api_request(
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: int,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log API request asynchronously to avoid blocking"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO api_logs (endpoint, method, status_code, response_time_ms, user_id, ip_address, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (endpoint, method, status_code, response_time_ms, user_id, ip_address, user_agent)
                )
                conn.commit()
        except Exception as e:
            # Don't let monitoring failures break the API
            logger.error(f"Failed to log API request: {e}")

    @staticmethod
    def get_api_stats(hours: int = 24):
        """Get API usage statistics"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    endpoint,
                    method,
                    COUNT(*) as request_count,
                    AVG(response_time_ms) as avg_response_time,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count
                FROM api_logs 
                WHERE created_at >= NOW() - INTERVAL '%s hours'
                GROUP BY endpoint, method
                ORDER BY request_count DESC
                """,
                (hours,)
            )
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_error_rates(hours: int = 24):
        """Get error rates by endpoint"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    endpoint,
                    COUNT(*) as total_requests,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count,
                    ROUND(COUNT(CASE WHEN status_code >= 400 THEN 1 END) * 100.0 / COUNT(*), 2) as error_rate
                FROM api_logs 
                WHERE created_at >= NOW() - INTERVAL '%s hours'
                GROUP BY endpoint
                HAVING COUNT(*) > 0
                ORDER BY error_rate DESC
                """,
                (hours,)
            )
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]