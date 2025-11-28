$env:PGPASSWORD = 'admin'
& 'C:\Program Files\PostgreSQL\18\bin\createdb.exe' -U postgres product_importer
Write-Host "Database created successfully!" -ForegroundColor Green
