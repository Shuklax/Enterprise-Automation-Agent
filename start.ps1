Write-Host "Starting Enterprise Automation Agent..." -ForegroundColor Green
Set-Location -Path "app"
uvicorn main:app --reload --port 8000