# Automated YouTube Music Liked Songs Torrent Downloader

A Windows tool that extracts all songs from YouTube Music "Liked songs" library and searches for a matching torrent via the command-line tool `torlink`.

## Setup & Usage

This is a one-click solution.

1. Review and adjust `config.yaml` as needed (e.g. enable SLM mode).
2. Double-click `bootstrap.bat`.
   - It will automatically check for Google Chrome and install it if missing.
   - It will install all dependencies in a virtual environment.
   - It will run the extractor. (Chrome will open; please log in to your Google account when prompted).
   - It will then start the orchestrator to begin downloading.

## Modes

- **Standard CLI Mode**: Attempts to interact with `torlink` programmatically.
- **SLM Mode**: Uses Ollama and a local Vision Language Model to read the terminal via screenshots and navigate the tool. Enable this in `config.yaml` by setting `use_slm: true`.
