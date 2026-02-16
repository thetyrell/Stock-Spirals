@echo off
REM Spiral Stock Chart - Quick Start Script for Windows

echo =========================================
echo Spiral Stock Chart - Local Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3 from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    pause
    exit /b 1
)

echo [OK] pip found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

REM Start the backend server
echo.
echo Starting backend server...
start "Backend Server" python backend.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start a simple HTTP server for the frontend
echo.
echo Starting frontend server...
start "Frontend Server" python -m http.server 8080

timeout /t 2 /nobreak >nul

echo.
echo =========================================
echo Application is ready!
echo =========================================
echo.
echo Open your browser and visit:
echo    http://localhost:8080/index.html
echo.
echo Backend API is running at:
echo    http://localhost:5000
echo.
echo Close the command windows to stop the servers
echo.
pause
