$env:PGPASSWORD = 'Sangh@2701'
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres product_importer
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database 'product_importer' created successfully!" -ForegroundColor Green
}
else {
    Write-Host "ℹ️  Database might already exist, checking..." -ForegroundColor Yellow
    & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d product_importer -c "SELECT 1;" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database 'product_importer' exists and is accessible!" -ForegroundColor Green
    }
}
