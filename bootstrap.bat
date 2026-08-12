@echo off
echo Starting YouTube Music Downloader...

:: Check for python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.10+ from python.org or via winget.
    pause
    exit /b
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

:: Check for node (for torlink)
node -v >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed. Please install Node.js from nodejs.org or via winget.
    pause
    exit /b
)

:: Check for Ollama
ollama --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Ollama is not installed. If you plan to use SLM mode, please install Ollama from ollama.com.
) ELSE (
    echo Checking for LLaVA model for SLM mode...
    ollama pull llava:7b
)

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
