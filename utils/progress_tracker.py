import redis
from config import settings
import json

# Redis client for progress tracking
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class ProgressTracker:
    """Utility class for tracking task progress in Redis"""
    
    @staticmethod
    def set_progress(task_id: str, progress: int, status: str, total: int = 100):
        """
        Set progress for a task
        
        Args:
            task_id: Unique task identifier
            progress: Current progress (0-100 or actual count)
            status: Status message
            total: Total items to process
        """
        data = {
            "progress": progress,
            "status": status,
            "total": total,
            "percentage": int((progress / total) * 100) if total > 0 else 0
        }
        redis_client.setex(
            f"progress:{task_id}",
            3600,  # Expire after 1 hour
            json.dumps(data)
        )
    
    @staticmethod
    def get_progress(task_id: str):
        """
        Get progress for a task
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            dict: Progress data or None if not found
        """
        data = redis_client.get(f"progress:{task_id}")
        if data:
            return json.loads(data)
        return None
    
    @staticmethod
    def set_error(task_id: str, error_message: str):
        """
        Set error status for a task
        
        Args:
            task_id: Unique task identifier
            error_message: Error message
        """
        data = {
            "progress": 0,
            "status": "error",
            "error": error_message,
            "percentage": 0
        }
        redis_client.setex(
            f"progress:{task_id}",
            3600,
            json.dumps(data)
        )
    
    @staticmethod
    def set_complete(task_id: str, message: str = "Complete"):
        """
        Mark task as complete
        
        Args:
            task_id: Unique task identifier
            message: Completion message
        """
        data = {
            "progress": 100,
            "status": "complete",
            "message": message,
            "percentage": 100
        }
        redis_client.setex(
            f"progress:{task_id}",
            3600,
            json.dumps(data)
        )
    
    @staticmethod
    def delete_progress(task_id: str):
        """
        Delete progress data for a task
        
        Args:
            task_id: Unique task identifier
        """
        redis_client.delete(f"progress:{task_id}")
