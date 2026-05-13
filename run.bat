@echo off
REM Session Manager Service - Quick Run Script for Windows
REM This script activates the virtual environment and starts the server

echo ========================================
echo Session Manager Service
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first or create venv manually:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [INFO] Virtual environment activated
echo.

REM Start the server
echo [INFO] Starting Session Manager Service...
echo [INFO] Server will be available at: http://localhost:8000
echo [INFO] API Documentation: http://localhost:8000/docs
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

uvicorn app.main:app --reload

REM If server stops
echo.
echo ========================================
echo Server stopped
echo ========================================
pause
