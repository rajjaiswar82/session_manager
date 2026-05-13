@echo off
REM Session Manager Service - Setup Script for Windows
REM This script sets up the complete development environment

echo ========================================
echo Session Manager Service - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo [OK] Python is installed
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist "venv" (
    echo [INFO] Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check PostgreSQL
echo [5/5] Checking PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL from https://www.postgresql.org/download/windows/
    echo.
    echo After installing PostgreSQL:
    echo 1. Create database: CREATE DATABASE session_manager;
    echo 2. Update .env file with your PostgreSQL password
    echo.
) else (
    psql --version
    echo [OK] PostgreSQL is installed
    echo.
    echo [INFO] Next steps:
    echo 1. Create database: psql -U postgres -c "CREATE DATABASE session_manager;"
    echo 2. Update .env file with your PostgreSQL password
    echo 3. Run: run.bat
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update .env file with your database credentials
echo 2. Create PostgreSQL database: session_manager
echo 3. Run: run.bat
echo 4. Open browser: http://localhost:8000/docs
echo.
pause
