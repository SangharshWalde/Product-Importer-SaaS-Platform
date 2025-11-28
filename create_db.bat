@echo off
echo Creating PostgreSQL database...
"C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres product_importer
if %errorlevel% == 0 (
    echo Database created successfully!
) else (
    echo Database might already exist or password is incorrect
    echo Trying to connect to verify...
    "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d product_importer -c "SELECT 1;"
)
