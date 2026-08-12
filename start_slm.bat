@echo off
echo Starting YouTube Music Downloader (SLM Mode)...

if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run bootstrap.bat first.
    pause
    exit /b
)

call venv\Scripts\activate.bat

echo.
echo ========================================
echo Starting the extractor...
echo ========================================
echo.

python extract_liked_songs.py

echo.
echo ========================================
echo Extraction complete. Starting the downloader in SLM Mode...
echo ========================================
echo.

python orchestrator.py --slm

echo.
echo ========================================
echo All tasks finished!
echo ========================================
pause
