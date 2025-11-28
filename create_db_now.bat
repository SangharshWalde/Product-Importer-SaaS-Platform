@echo off
set PGPASSWORD=Sangh@2701
"C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres product_importer
if %errorlevel% == 0 (
    echo Database created successfully!
) else (
    echo Database might already exist, verifying...
    "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d product_importer -c "SELECT 1;" >nul 2>&1
    if %errorlevel% == 0 (
        echo Database exists and is accessible!
    ) else (
        echo Error: Could not create or access database
    )
)
