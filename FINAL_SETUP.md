# Product Importer SaaS - Final Setup Steps

## ✅ What's Complete

1. ✅ **Python Environment** - Virtual environment created with all dependencies
2. ✅ **Redis Server** - Downloaded, extracted, and verified running
3. ✅ **PostgreSQL** - Service running on port 5432
4. ✅ **Startup Scripts** - Created for easy application launch

## ⚠️ One Final Step Required

### Create PostgreSQL Database

You need to create the database `product_importer`. Choose ONE method:

#### **Option 1: Using pgAdmin (Easiest - GUI)**
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to PostgreSQL server
3. Right-click "Databases" → Create → Database
4. Name: `product_importer`
5. Click Save

#### **Option 2: Using Command Line**
Open a new PowerShell window and run:
```powershell
# You'll be prompted for your PostgreSQL password
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres product_importer
```

#### **Option 3: Using psql**
```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
# Then in the psql prompt:
CREATE DATABASE product_importer;
\q
```

---

## 🚀 Running the Application

### Step 1: Update .env File
Edit `c:\Product-Importer-SaaS\.env` and replace `admin` with your actual PostgreSQL password:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/product_importer
```

### Step 2: Start Backend Server
Open PowerShell in the project directory:
```powershell
.\start_backend.ps1
```

This will:
- Start Redis automatically
- Launch FastAPI on http://localhost:8000
- Create database tables automatically

### Step 3: Start Celery Worker (New Terminal)
Open a **second** PowerShell window:
```powershell
cd c:\Product-Importer-SaaS
.\start_celery.ps1
```

### Step 4: Access Application
Open your browser: **http://localhost:8000**

---

## 📁 Project Files Created

- `start_backend.ps1` - Starts Redis + FastAPI backend
- `start_celery.ps1` - Starts Celery worker
- `redis/` - Redis server files
- `.env` - Configuration file (update password!)

---

## 🧪 Quick Test

1. Open http://localhost:8000
2. Upload `sample_products.csv`
3. Watch real-time progress tracking!

---

## 🐛 Troubleshooting

### "Cannot connect to database"
- Verify database `product_importer` exists
- Check PostgreSQL password in `.env` file
- Ensure PostgreSQL service is running

### "Cannot connect to Redis"
- Redis starts automatically with `start_backend.ps1`
- Or manually run: `.\redis\redis-server.exe`

### Application won't start
- Make sure database is created first
- Check `.env` file has correct password
- Verify both PostgreSQL and Redis are running

---

## 📊 System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Python 3.13.5 | ✅ | Virtual environment ready |
| Dependencies | ✅ | All packages installed |
| Redis | ✅ | Running on port 6379 |
| PostgreSQL | ✅ | Running on port 5432 |
| Database | ⚠️ | **Create manually** |
| .env Config | ⚠️ | **Update password** |

---

## 🎯 Summary

**You're almost done!** Just:
1. Create database `product_importer` (2 minutes)
2. Update password in `.env` (30 seconds)
3. Run `.\start_backend.ps1`
4. Run `.\start_celery.ps1` in new terminal
5. Open http://localhost:8000

Enjoy your Product Importer SaaS! 🎉
