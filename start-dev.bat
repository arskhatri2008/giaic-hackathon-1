@echo off
REM Script to start both frontend and backend servers simultaneously

echo Starting Physical AI & Humanoid Robotics application...
echo.

REM Start backend server in background
echo Starting backend server on port 8000...
start "Backend Server" cmd /c "cd backend && python -c \"from api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)\""

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server
echo Starting frontend server on port 3000...
cd website && npm run start

pause