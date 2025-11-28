# Start Celery Worker
Write-Host "⚙️  Starting Celery Worker..." -ForegroundColor Cyan
Write-Host "Make sure Redis is running before starting Celery`n" -ForegroundColor Yellow

# Test Redis first
$redisTest = & ".\redis\redis-cli.exe" ping 2>$null
if ($redisTest -ne "PONG") {
    Write-Host "❌ Redis is not running! Please start Redis first." -ForegroundColor Red
    Write-Host "Run: .\start_backend.ps1 in another terminal" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Redis is running!" -ForegroundColor Green
Write-Host "`nStarting Celery worker...`n" -ForegroundColor Cyan

& ".\venv\Scripts\python.exe" -m celery -A celery_app worker --loglevel=info --pool=solo
