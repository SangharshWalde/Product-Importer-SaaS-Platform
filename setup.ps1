# Quick Start Script for Product Importer SaaS

Write-Host "🚀 Product Importer SaaS - Quick Start" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "⚙️  Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created! Please update with your database credentials." -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update .env file with your PostgreSQL and Redis credentials" -ForegroundColor White
Write-Host "2. Ensure PostgreSQL is running" -ForegroundColor White
Write-Host "3. Ensure Redis is running" -ForegroundColor White
Write-Host "4. Run: uvicorn app:app --reload" -ForegroundColor White
Write-Host "5. In a new terminal, run: celery -A celery_app worker --loglevel=info --pool=solo" -ForegroundColor White
Write-Host "6. Open http://localhost:8000 in your browser" -ForegroundColor White
Write-Host ""
