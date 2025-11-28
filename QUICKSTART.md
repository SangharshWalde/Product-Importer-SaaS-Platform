# 🚀 Quick Start Guide - Product Importer SaaS

## ✅ What's Already Done

- ✅ Virtual environment created (`venv/`)
- ✅ All Python dependencies installed
- ✅ `.env` configuration file created
- ✅ PostgreSQL 18 is running

## ⚠️ What You Need to Do

### 1. Install Redis (Required for Celery)

**Fastest Option**: Download Redis for Windows
- Visit: https://github.com/microsoftarchive/redis/releases
- Download: `Redis-x64-3.0.504.msi`
- Run installer
- Redis will start automatically as a Windows service

See [REDIS_INSTALL.md](file:///c:/Product-Importer-SaaS/REDIS_INSTALL.md) for other options (WSL2, Memurai)

### 2. Create Database

**Easiest Option**: Use pgAdmin
1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Name: `product_importer`
4. Save

See [DATABASE_SETUP.md](file:///c:/Product-Importer-SaaS/DATABASE_SETUP.md) for command-line options

### 3. Update .env File

Edit `c:\Product-Importer-SaaS\.env`:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/product_importer
REDIS_URL=redis://localhost:6379/0
```

**Replace `YOUR_PASSWORD`** with your PostgreSQL password!

## 🎯 Run the Application

### Terminal 1: Start Backend
```powershell
cd c:\Product-Importer-SaaS
.\venv\Scripts\Activate.ps1
uvicorn app:app --reload
```

### Terminal 2: Start Celery Worker
```powershell
cd c:\Product-Importer-SaaS
.\venv\Scripts\Activate.ps1
celery -A celery_app worker --loglevel=info --pool=solo
```

### Access Application
Open browser: http://localhost:8000

## 📝 Quick Test

Upload the included `sample_products.csv` to test the system!

## 🆘 Need Help?

- Redis installation: See [REDIS_INSTALL.md](file:///c:/Product-Importer-SaaS/REDIS_INSTALL.md)
- Database setup: See [DATABASE_SETUP.md](file:///c:/Product-Importer-SaaS/DATABASE_SETUP.md)
- Full details: See [walkthrough.md](file:///C:/Users/Sangharsh%20Walde/.gemini/antigravity/brain/71d2403f-f0b2-4a15-b9ae-16a6686dd3eb/walkthrough.md)
