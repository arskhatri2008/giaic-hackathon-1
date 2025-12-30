# PowerShell script to start both frontend and backend servers simultaneously

Write-Host "Starting Physical AI & Humanoid Robotics application..." -ForegroundColor Green
Write-Host ""

# Function to start backend server
function Start-Backend {
    Write-Host "Starting backend server on port 8000..." -ForegroundColor Yellow
    Start-Process -FilePath "cmd" -ArgumentList "/c", "cd backend && python -c `"from api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)`""
}

# Function to start frontend server
function Start-Frontend {
    Write-Host "Starting frontend server on port 3000..." -ForegroundColor Yellow
    Start-Process -FilePath "cmd" -ArgumentList "/c", "cd website && npm start"
}

# Start backend server
Start-Backend

# Wait for backend to start
Start-Sleep -Seconds 5

# Start frontend server
Start-Frontend

Write-Host "Both servers started successfully!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")