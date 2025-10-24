@echo off
COLOR 0A

echo ========================================
echo  UPGRADE TO GEMINI 2.0 FLASH THINKING
echo  (More Intelligent Biblical Chatbot)
echo ========================================
echo.

echo This script will upgrade your chatbot to use:
echo - Gemini 2.0 Flash Thinking Experimental
echo - Rated as world's best model
echo - Better theological understanding
echo - Deeper Jesus-believer context
echo - Still 100%% FREE!
echo.
pause

:: Step 1: Backup current backend
echo [1/5] Backing up current chatbot_backend.py...
if exist "chatbot_backend.py" (
    copy chatbot_backend.py chatbot_backend_llama_backup.py >nul
    echo [OK] Backup created: chatbot_backend_llama_backup.py
) else (
    echo [WARNING] chatbot_backend.py not found
)
echo.

:: Step 2: Install enhanced version
echo [2/5] Installing enhanced Gemini version...
if exist "chatbot_backend_gemini_enhanced.py" (
    copy chatbot_backend_gemini_enhanced.py chatbot_backend.py >nul
    echo [OK] Enhanced version installed
) else (
    echo [ERROR] chatbot_backend_gemini_enhanced.py not found!
    echo Please download it first.
    pause
    exit /b 1
)
echo.

:: Step 3: Get API key
echo [3/5] Setting up Google AI Studio API Key...
echo.
echo Please follow these steps:
echo 1. Visit: https://aistudio.google.com/apikey
echo 2. Sign in with your Google account (FREE)
echo 3. Click "Create API Key"
echo 4. Copy the key (starts with AI...)
echo.
set /p api_key="Paste your Google API Key here: "

if "%api_key%"=="" (
    echo [WARNING] No API key provided!
    echo You'll need to set it manually in chatbot_backend.py
    echo Or set environment variable: GOOGLE_API_KEY
    pause
) else (
    :: Save to environment for this session
    set GOOGLE_API_KEY=%api_key%
    echo [OK] API key set for this session

    :: Update the file with the key
    powershell -Command "(Get-Content chatbot_backend.py) -replace 'YOUR_GOOGLE_API_KEY_HERE', '%api_key%' | Set-Content chatbot_backend.py"
    echo [OK] API key embedded in chatbot_backend.py
)
echo.

:: Step 4: Test connection
echo [4/5] Testing Gemini connection...
python -c "from openai import OpenAI; import os; client = OpenAI(base_url='https://generativelanguage.googleapis.com/v1beta/openai/', api_key=os.environ.get('GOOGLE_API_KEY')); print('[OK] Connection successful!')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Could not test connection
    echo Make sure your API key is correct
)
echo.

:: Step 5: Done
echo [5/5] Upgrade complete!
echo.
echo ========================================
echo  UPGRADE SUCCESSFUL!
echo ========================================
echo.
echo Your chatbot now uses:
echo - Gemini 2.0 Flash Thinking Experimental
echo - Advanced theological reasoning
echo - Better Bible verse understanding
echo - Jesus-centered contextual answers
echo.
echo To start the enhanced chatbot:
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo.
echo ========================================
echo.
echo You can always switch back by running:
echo   copy chatbot_backend_llama_backup.py chatbot_backend.py
echo.
pause
