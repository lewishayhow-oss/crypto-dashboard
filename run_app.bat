@echo off
SETLOCAL EnableDelayedExpansion
TITLE CryptoDashboard Launcher

:: --- SHORT PATH FIX FOR WINDOWS ---
:: Python 3.14 builds fail on deep paths. We use a virtual drive (Z:) to shorten them.
if /I "%CD:~0,2%" NEQ "Z:" (
    echo [Setup] Mounting project to virtual drive Z: to fix path length issues...
    subst Z: .
    if exist Z:\ (
        Z:
        cd \
        call run_app.bat
        :: Cleanup after the recursive call returns
        c:
        subst Z: /d >nul 2>nul
        exit /b
    ) else (
        echo [WARNING] Could not mount Z: drive. Attempting to run normally...
    )
)
:: ----------------------------------

echo ===================================================
echo      CryptoDashboard - Automatic Setup and Run
echo ===================================================
echo.

:: 1. Check if Node is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install it from nodejs.org
    pause
    exit /b
)

:: 2. Setup Frontend (if missing)
if not exist "market-stream\frontend\node_modules\" (
    echo [First Run] Installing Frontend dependencies...
    pushd market-stream\frontend
    call npm install
    popd
    echo [OK] Frontend ready.
    echo.
)

:: 3. Setup Backend (if missing)
if not exist "venv\" (
    echo [First Run] Creating Python virtual environment...
    python -m venv venv
    
    echo [First Run] Installing Python libraries...
    call venv\Scripts\activate.bat
    :: We upgrade pip first to handle new Python versions better
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo [OK] Backend ready.
    echo.
)

:: 4. Run the App
echo Starting Engine, API, and Frontend...
echo (Press Ctrl+C to close all windows)
echo.

:: Run concurrently
call npx -y concurrently -k -n "ENGINE,API,UI" -c "blue,magenta,green" "venv\Scripts\python market-stream/data-engine/server.py" "venv\Scripts\python market-stream/api-gateway/app.py" "npm run dev --prefix market-stream/frontend"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application stopped unexpectedly.
    pause
)