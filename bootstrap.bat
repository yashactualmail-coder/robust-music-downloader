@echo off
echo Starting YouTube Music Downloader (yt-dlp version)...

:: Check for python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.10+ from python.org or via winget.
    pause
    exit /b
)

:: Check for Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" goto chrome_installed
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" goto chrome_installed
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" goto chrome_installed

echo Google Chrome is not installed. Installing via winget...
winget install Google.Chrome -e --accept-source-agreements --accept-package-agreements
:chrome_installed

:: Check for FFmpeg (needed for yt-dlp audio extraction)
ffmpeg -version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo FFmpeg is not installed. Installing via winget...
    winget install Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
    echo IMPORTANT: FFmpeg has been installed. You may need to restart your terminal or PC for it to be recognized in your PATH.
)

:: Create venv if not exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv and install requirements
echo Activating virtual environment and installing requirements...
call venv\Scripts\activate.bat
call pip install --upgrade pip
call pip install -r requirements.txt

echo.
echo ========================================
echo Dependencies installed and environment ready.
echo Starting the extractor...
echo ========================================
echo.

python extract_liked_songs.py

echo.
echo ========================================
echo Extraction complete. Starting the downloader...
echo ========================================
echo.

python orchestrator.py

echo.
echo ========================================
echo All tasks finished!
echo ========================================
pause
