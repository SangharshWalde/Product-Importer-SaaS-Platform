# Database Setup Guide

## Create PostgreSQL Database

### Option 1: Using pgAdmin (GUI - Easiest)
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to your PostgreSQL server
3. Right-click on "Databases"
4. Select "Create" → "Database"
5. Name: `product_importer`
6. Click "Save"

### Option 2: Using Command Line
```powershell
# Open PowerShell and run:
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
```

When prompted for password, enter your PostgreSQL password (likely: `admin` or `postgres`)

Then in the PostgreSQL prompt:
```sql
CREATE DATABASE product_importer;
\l
-- You should see product_importer in the list
\q
```

### Option 3: Using createdb Command
```powershell
# Set your password (replace 'admin' with your actual password)
$env:PGPASSWORD = 'admin'

# Create the database
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres product_importer

# Verify
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -l
```

## Update .env File

Edit `c:\Product-Importer-SaaS\.env`:

```env
# Replace 'admin' with your actual PostgreSQL password
DATABASE_URL=postgresql://postgres:admin@localhost:5432/product_importer
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here-change-in-production
UPLOAD_DIR=uploads
MAX_FILE_SIZE=104857600
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

## Verify Database Connection

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Test database connection
python -c "from sqlalchemy import create_engine; import os; from dotenv import load_dotenv; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✅ Database connection successful!'); conn.close()"
```
