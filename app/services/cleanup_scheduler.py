import asyncio
import threading
from datetime import datetime, timedelta
from app.services.location_service import LocationService
from app.utils.logger import logger

class CleanupScheduler:
    def __init__(self):
        self.location_service = LocationService()
        self.is_running = False
        self.cleanup_thread = None

    def start(self):
        """Start the cleanup scheduler"""
        if not self.is_running:
            self.is_running = True
            self.cleanup_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.cleanup_thread.start()
            logger.info("Cleanup scheduler started")

    def stop(self):
        """Stop the cleanup scheduler"""
        self.is_running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
        logger.info("Cleanup scheduler stopped")

    def _run_scheduler(self):
        """Run the cleanup scheduler loop"""
        while self.is_running:
            try:
                # Run cleanup every hour
                self._run_cleanup()
                
                # Sleep for 1 hour (3600 seconds)
                for _ in range(3600):
                    if not self.is_running:
                        break
                    threading.Event().wait(1)  # Sleep 1 second at a time to allow quick shutdown
                    
            except Exception as e:
                logger.error(f"Cleanup scheduler error: {e}")
                # Sleep for 5 minutes before retrying
                threading.Event().wait(300)

    def _run_cleanup(self):
        """Execute cleanup tasks"""
        try:
            logger.info("Starting scheduled cleanup...")
            
            # Clean up old location records
            self.location_service.cleanup_old_locations()
            
            logger.info("Scheduled cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup task failed: {e}")

    def run_manual_cleanup(self):
        """Run cleanup manually (for testing or admin trigger)"""
        try:
            self._run_cleanup()
            return {"message": "Manual cleanup completed successfully"}
        except Exception as e:
            logger.error(f"Manual cleanup failed: {e}")
            return {"error": f"Cleanup failed: {str(e)}"}

# Global cleanup scheduler instance
cleanup_scheduler = CleanupScheduler()