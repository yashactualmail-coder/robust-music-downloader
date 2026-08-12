@echo off
echo Setting up YouTube Music Downloader...

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
pip install --upgrade pip
pip install -r requirements.txt

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
    echo Pulling LLaVA model for SLM mode (this might take a while if not already downloaded)...
    ollama pull llava:7b
)

echo Setup complete. To run the app, activate the venv (venv\Scripts\activate.bat) and run python orchestrator.py
pause
