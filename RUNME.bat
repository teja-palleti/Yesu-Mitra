@echo off
echo ========================================
echo Yesu Mitra Biblical Chatbot
echo ========================================
echo.

echo [Step 1/3] Installing dependencies...
pip install openai gtts flask
echo.

echo [Step 2/3] Downloading Telugu Bible data...
python download_telugu_bible.py
echo.

echo [Step 3/3] Starting the chatbot...
python app.py

pause
