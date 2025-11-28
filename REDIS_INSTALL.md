# Quick Redis Installation Guide for Windows

## Option 1: Download Redis for Windows (Recommended - Fastest)

### Step 1: Download
Visit: https://github.com/microsoftarchive/redis/releases
Download: Redis-x64-3.0.504.msi (or latest version)

### Step 2: Install
- Run the MSI installer
- Accept defaults
- Redis will install as a Windows service

### Step 3: Verify
```powershell
Get-Service Redis
```

---

## Option 2: Install WSL2 + Redis (Most Compatible)

### Step 1: Install WSL2
```powershell
# Run as Administrator
wsl --install
```
**Note**: Restart your computer after installation

### Step 2: Install Redis in WSL2
```bash
# After restart, open WSL2 terminal
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
```

### Step 3: Verify
```bash
redis-cli ping
# Should return: PONG
```

---

## Option 3: Use Memurai (Redis Alternative for Windows)

### Download and Install
Visit: https://www.memurai.com/get-memurai
Download and run the installer

### Verify
```powershell
Get-Service Memurai
```

---

## After Installation

Update your `.env` file:
```env
# If using Redis on Windows or Memurai
REDIS_URL=redis://localhost:6379/0

# If using WSL2
REDIS_URL=redis://localhost:6379/0
```

## Test Redis Connection
```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Test with Python
python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); print(r.ping())"
```

If you see `True`, Redis is working! ✅
