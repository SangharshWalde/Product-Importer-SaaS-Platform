#!/bin/bash

# Start Celery Worker in background
celery -A celery_app worker --loglevel=info --concurrency=1 &

# Start Web Server
uvicorn app:app --host 0.0.0.0 --port $PORT --proxy-headers
