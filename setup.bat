@echo off
REM Setup script for GrayVideo Enhanced on Windows

echo.
echo ==========================================
echo GrayVideo Enhanced - Setup Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Create snapshots directory
if not exist snapshots (
    mkdir snapshots
    echo [OK] Snapshots directory created
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start using GrayVideo Enhanced:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo   2. Run the application:
echo      python video_processor.py
echo.
echo For help with command-line options:
echo   python video_processor.py --help
echo.
pause
