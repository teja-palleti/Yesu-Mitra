@echo off
SETLOCAL EnableDelayedExpansion
COLOR 0A

:: ============================================
:: Yesu Mitra Biblical Chatbot - Complete Setup & Run
:: ============================================

echo.
echo ========================================
echo    YESU MITRA BIBLICAL CHATBOT
echo    Complete Setup and Run Script
echo ========================================
echo.

:: Step 1: Check Python Installation
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python is installed
echo.

:: Step 2: Check pip
echo [2/7] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] pip is not available!
    echo Attempting to install pip...
    python -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo [ERROR] Could not install pip!
        pause
        exit /b 1
    )
)
echo [OK] pip is available
echo.

:: Step 3: Check/Install Dependencies
echo [3/7] Checking and installing dependencies...
echo.
echo Installing: openai, gtts, flask...
pip install --quiet openai gtts flask
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Some dependencies may have failed to install
    echo Attempting to upgrade pip and retry...
    python -m pip install --upgrade pip
    pip install openai gtts flask
)
echo [OK] Dependencies installed
echo.

:: Step 4: Check Project Files
echo [4/7] Checking project files...
set FILES_OK=1

if not exist "app.py" (
    echo [ERROR] app.py not found!
    set FILES_OK=0
)
if not exist "chatbot_backend.py" (
    echo [ERROR] chatbot_backend.py not found!
    set FILES_OK=0
)
if not exist "templates\index.html" (
    echo [WARNING] templates\index.html not found!
    echo Checking if index.html exists in current directory...
    if exist "index.html" (
        echo [FIX] Creating templates folder and moving index.html...
        mkdir templates 2>nul
        copy index.html templates\index.html >nul
        echo [OK] index.html copied to templates folder
    ) else (
        echo [ERROR] index.html not found anywhere!
        set FILES_OK=0
    )
)

if !FILES_OK! equ 0 (
    echo.
    echo [ERROR] Required project files are missing!
    echo Please ensure you have extracted all files from the ZIP.
    echo.
    pause
    exit /b 1
)
echo [OK] All project files present
echo.

:: Step 5: Check/Download Telugu Bible Data
echo [5/7] Checking Telugu Bible data...
if not exist "telugu_bible.json" (
    echo [WARNING] telugu_bible.json not found!
    echo.

    :: Check for fixed download script first
    if exist "download_telugu_bible_fixed.py" (
        echo [ACTION] Downloading Telugu Bible data (using fixed script)...
        echo This will download 11.2 MB from GitHub...
        echo.
        python download_telugu_bible_fixed.py
        if %errorlevel% neq 0 (
            echo.
            echo [WARNING] Fixed download script failed, trying alternative...
        )
    )

    :: If still not found, try original script
    if not exist "telugu_bible.json" (
        if exist "download_telugu_bible.py" (
            echo [ACTION] Trying alternative download method...
            python download_telugu_bible.py
        )
    )

    :: Final check
    if not exist "telugu_bible.json" (
        echo.
        echo [ERROR] Failed to download Bible data!
        echo.
        echo MANUAL DOWNLOAD REQUIRED:
        echo 1. Visit: https://github.com/godlytalias/Bible-Database
        echo 2. Navigate to: Telugu folder
        echo 3. Download: bible.json
        echo 4. Save as: telugu_bible.json in this folder
        echo.
        echo After downloading, run this script again.
        echo.
        pause
        exit /b 1
    )
) else (
    echo [OK] telugu_bible.json found
)
echo.

:: Step 6: Verify API Key
echo [6/7] Verifying Groq API key configuration...
findstr /C:"gsk_" chatbot_backend.py >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Groq API key may not be configured!
    echo.
    echo Please ensure your API key is set in chatbot_backend.py
    echo or set as environment variable GROQ_API_KEY
    echo.
) else (
    echo [OK] API key appears to be configured
)
echo.

:: Step 7: Start the Chatbot
echo [7/7] Starting Yesu Mitra Chatbot...
echo.
echo ========================================
echo    CHATBOT IS STARTING...
echo ========================================
echo.
echo [INFO] The web server will start on: http://localhost:5000
echo [INFO] Press CTRL+C to stop the server
echo.
echo Once started, open your browser and go to:
echo.
echo     http://localhost:5000
echo.
echo ========================================
echo.

:: Give user a moment to read
timeout /t 3 /nobreak >nul

:: Start the chatbot
python app.py

:: If the script exits, show error
echo.
echo ========================================
echo    CHATBOT STOPPED
echo ========================================
echo.
echo If you see errors above, please check:
echo 1. All dependencies are installed
echo 2. telugu_bible.json exists
echo 3. Groq API key is configured
echo 4. Port 5000 is not already in use
echo.
echo For detailed help, see README.md
echo.
pause
