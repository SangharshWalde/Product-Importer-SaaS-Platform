# Start Redis Server
Write-Host "🚀 Starting Redis Server..." -ForegroundColor Cyan
Start-Process -FilePath ".\redis\redis-server.exe" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Test Redis
$redisTest = & ".\redis\redis-cli.exe" ping
if ($redisTest -eq "PONG") {
    Write-Host "✅ Redis is running!" -ForegroundColor Green
}
else {
    Write-Host "❌ Redis failed to start" -ForegroundColor Red
    exit 1
}

# Activate virtual environment and start FastAPI
Write-Host "`n🌐 Starting FastAPI Backend..." -ForegroundColor Cyan
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Gray

& ".\venv\Scripts\python.exe" -m uvicorn app:app --reload
