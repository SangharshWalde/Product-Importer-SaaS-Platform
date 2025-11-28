from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from config import settings
from tasks import process_csv_file
from utils import validate_csv_headers, ProgressTracker
import pandas as pd

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload CSV file for product import
    
    Args:
        file: CSV file to upload
        
    Returns:
        JSON response with task_id for progress tracking
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Check file size (read in chunks to avoid memory issues)
        file_size = 0
        chunk_size = 1024 * 1024  # 1MB chunks
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.csv")
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Validate CSV headers
        try:
            df = pd.read_csv(file_path, nrows=1)
            headers = df.columns.tolist()
            is_valid, error_msg = validate_csv_headers(headers)
            
            if not is_valid:
                os.remove(file_path)
                raise HTTPException(status_code=400, detail=error_msg)
        except pd.errors.EmptyDataError:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="CSV file is empty")
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Initialize progress immediately to avoid "waiting" state
        ProgressTracker.set_progress(task_id, 0, "Queued for processing...", 100)
        
        # Start background task
        process_csv_file.delay(file_path, task_id)
        
        return JSONResponse(
            status_code=202,
            content={
                "message": "File uploaded successfully. Processing started.",
                "task_id": task_id
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
