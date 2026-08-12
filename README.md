# Automated YouTube Music Liked Songs Torrent Downloader

A Windows tool that extracts all songs from YouTube Music "Liked songs" library and searches for a matching torrent via the command-line tool `torlink`.

## Setup

1. Run `bootstrap.bat` to create the virtual environment and install dependencies.
2. Review and adjust `config.yaml` as needed.

## Usage

1. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate.bat
   ```
2. Extract your liked songs from YouTube Music:
   ```cmd
   python extract_liked_songs.py
   ```
   (This will open Chrome. Log in to your Google account when prompted).
3. Start the orchestrator to begin downloading:
   ```cmd
   python orchestrator.py
   ```

## Modes

- **Standard CLI Mode**: Attempts to interact with `torlink` programmatically.
- **SLM Mode**: Uses Ollama and a local Vision Language Model to read the terminal via screenshots and navigate the tool. Enable this in `config.yaml` by setting `use_slm: true`.
