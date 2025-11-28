from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils import ProgressTracker
import asyncio
import json

router = APIRouter()


@router.get("/progress/{task_id}")
async def get_progress(task_id: str):
    """
    Server-Sent Events endpoint for real-time progress tracking
    
    Args:
        task_id: Task identifier
        
    Returns:
        SSE stream with progress updates
    """
    async def event_generator():
        tracker = ProgressTracker()
        
        while True:
            # Get progress from Redis
            progress_data = tracker.get_progress(task_id)
            
            if progress_data:
                # Send progress update
                yield f"data: {json.dumps(progress_data)}\n\n"
                
                # Check if complete or error
                if progress_data.get("status") in ["complete", "error"]:
                    break
            else:
                # No progress data yet
                yield f"data: {json.dumps({'status': 'waiting', 'percentage': 0})}\n\n"
            
            # Wait before next update
            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
