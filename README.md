# Automated YouTube Music Liked Songs Downloader

A Windows tool that extracts all songs from your YouTube Music "Liked songs" library and downloads them directly in lossless FLAC format using `yt-dlp`.

## Features
- **One-Click Setup:** Automatically installs Google Chrome, FFmpeg, and Python dependencies.
- **Bypasses Google Anti-Bot:** Uses `undetected-chromedriver` to securely log into your account, and routes `yt-dlp` requests via IPv4 while spoofing the Android client to completely bypass YouTube's 403 Forbidden blocks.
- **Interactive Terminal UI:** Review and select exactly which songs you want to download using an interactive checklist before the process begins.
- **Highest Quality:** Extracts audio in lossless FLAC format straight from YouTube's backend.

## Setup & Usage

This is a one-click solution.

1. Double-click `bootstrap.bat`.
   - It will check for and install Google Chrome and FFmpeg (via `winget`) if they are missing.
   - It will install all necessary Python dependencies in a virtual environment.
   - It will launch a secure browser. **Please log into your Google account when prompted**, navigate to your Liked Songs, and press **Enter** in the terminal to begin extraction.
   - After extracting your library, you will be presented with an interactive checklist in the terminal.
2. **Select your songs:** Use the **Arrow keys** to navigate, **Spacebar** to select/deselect songs, and **Enter** to confirm.
3. The script will automatically download the selected songs directly to the `downloads/` folder.

If you ever interrupt the process, your progress is saved in `progress.json`. To re-download songs that were already marked as complete, simply delete `progress.json` before running the script.
