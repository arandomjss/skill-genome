cd $PSScriptRoot
Write-Host "Starting FastAPI server..."
Write-Host "Server will be available at: http://localhost:8000"
Write-Host "API docs at: http://localhost:8000/docs"
Write-Host ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
