@echo off
echo =====================================
echo   MoodTunes Corporate VPN Solution
echo =====================================
echo.

REM Check if ngrok exists
if not exist "ngrok.exe" (
    echo ❌ ngrok.exe not found!
    echo.
    echo 📋 Please download ngrok:
    echo 1. Go to https://ngrok.com/download
    echo 2. Create free account
    echo 3. Download Windows version
    echo 4. Extract ngrok.exe to this folder
    echo.
    pause
    exit /b 1
)

echo ✅ Found ngrok.exe
echo.

echo 🚀 Starting MoodTunes server...
start "MoodTunes Server" /min py app.py

echo.
echo ⏳ Waiting for server to start...
timeout /t 3 /nobreak > nul

echo.
echo 🌐 Creating public tunnel with ngrok...
echo.
echo 📱 Your public URL will appear below:
echo =====================================
ngrok.exe http 5000

echo.
echo 🛑 MoodTunes stopped.
pause