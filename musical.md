# Automated YouTube Music Liked Songs Torrent Downloader – Development Plan (v2)

## 1. Overview
A Windows tool that:
1. Extracts all songs from **YouTube Music "Liked songs"** library.
2. For each song, searches for a matching torrent via the command‑line tool **`torlink`**, *verifies* the top result, and downloads it.
3. Uses a **local SLM (Small Language/Vision Model)** as an *optional* fallback to navigate `torlink` via screenshots and simulated keystrokes, making interaction robust even if the tool’s output format changes.
4. Handles mismatches gracefully by logging them to a manual intervention file.

---

## 2. Key Enhancements Over v1

- **Torrent verification before download** – prevents pulling completely wrong content.
- **SLM‑based navigation** (optional advanced mode) – enables fully vision‑based interaction with `torlink`, eliminating fragile output parsing.
- **Explicit bootstrap** – the tool will install missing dependencies (Python, Ollama, models, etc.) because the machines likely haven’t run such a stack before.

---

## 3. Assumptions & Prerequisites
- **Windows 10/11** with an NVIDIA GPU (at least GeForce RTX 3060 Laptop, 6 GB VRAM; lower tiers may work with quantized models).
- **`torlink`** is installed and can be navigated entirely by keyboard (arrow keys, Enter, Tab, etc.). It can be launched from any terminal (CMD, PowerShell, Windows Terminal).
- The user has a YouTube Music account and is okay with using a persistent browser session.
- Internet connection is stable; the tool will pull dependencies (Python packages, model files) on first run.

---

## 4. High‑Level Architecture

```
[YouTube Music Web UI]  
        │  (Selenium)
        ▼
[Song List Extractor]  →  liked_songs.json
        │
        ▼
[Orchestrator] 
   │
   ├── For each song:
   │      ├── Search query → torlink CLI (or SLM-driven)
   │      ├── Parse top result name
   │      ├── Verification (fuzzy match ≥ 80%)
   │      │       ├── Pass → download (torlink or SLM)
   │      │       └── Fail → log to manual_downloads.txt
   │      └── Track progress
   │
   └── Optional: SLM module (local vision model) to navigate torlink via screenshots
```

---

## 5. Detailed Components

### 5.1 Bootstrap & Dependency Installation
Because the target machines likely have no prior setup, the tool will include a **bootstrap script** (`setup.bat` or PowerShell) that:
- Checks for Python 3.10+ and installs it (if missing) using the official embeddable package or `winget`.
- Installs required Python packages: `selenium`, `webdriver-manager`, `fuzzywuzzy`, `python-Levenshtein`, `pyautogui`, `tqdm`, `pyyaml`, `requests` (for Ollama API), `Pillow` (screenshot).
- Ensures Google Chrome is installed (prompts user if not).
- Installs **Ollama** (if SLM mode is desired) and pulls a suitable vision model (`llava:7b` or `bakllava`). The model file (~4‑8 GB) is downloaded once.
- Makes `torlink` available: the tool will execute `npx torlnk` (torlink is distributed as an npm package) to run it directly, or alternatively prompt the user to install it globally with `npm install -g torlnk`. The bootstrap script will check for Node.js/npm and install them if missing.

**Rationale:** No hand‑holding for end‑users; the script does it all.

---

### 5.2 Song List Extraction (YouTube Music)
*No major changes from v1 – Selenium with persistent Chrome profile.*

- Launch Chrome with `--user-data-dir` pointing to a custom profile folder (so the user can log in once).
- Navigate to `https://music.youtube.com/playlist?list=LM`.
- Scroll the playlist container until the count stabilises.
- Extract title and artist from the DOM (selectors may need occasional updating).
- Save to `liked_songs.json`.
- Add a delay between scrolls and a random mouse move to appear more human (reduces bot detection risk).

---

### 5.3 Torrent Search & Verification

**Search query construction:**  
`"{artist} - {title}"` optionally appended with ` mp3` if `torlink` supports it.

**Verification method:**  
After `torlink search "..."`, the tool reads the name of the top result (usually the first line).  
- Clean both the result name and the expected `"{artist} - {title}"`:
  - Lowercase, remove bracketed text (e.g., " (Official Video)"), strip extra spaces.
- Compute **fuzzy partial ratio** (using `fuzzywuzzy` / `partial_ratio`).  
- If **similarity ≥ 80%** → consider it a match and proceed to download.  
- If **similarity < 80%** → log the expected song, the top result name, and the search query to **`manual_downloads.txt`**. The song is skipped for now.  

This check happens *before* initiating any download, saving time and bandwidth.

**Download (non‑SLM path):**  
If the verification passes, the tool issues `torlink download <magnet_or_number>` and waits for completion (monitoring the process). Default behaviour of `torlink` should put the file into a configured output folder.

---

### 5.4 Optional Advanced Module: SLM‑Driven Navigation

**Goal:** Replace fragile CLI output parsing with a local vision model that sees the terminal and decides the next keystroke.

**How it works:**
1. A terminal window (or a hidden console) runs `torlink` (via `npx torlnk`). The tool captures a **screenshot** of that window after every command (using `pyautogui` or `PIL.ImageGrab`).
2. The screenshot is sent to a **local vision‑language model** (hosted via Ollama API at `http://localhost:11434`).  
   **Prompt template:**  
   ```
   You are controlling the CLI tool `torlink`. The current screen is shown.  
   We want to search for: "{artist} - {title}" and download the first result.  
   What single key should be pressed next? (UP, DOWN, ENTER, TAB, ESC, q)  
   Respond with only the key name.
   ```
3. The model returns the next action. The tool simulates that keypress (e.g., `pyautogui.press('down')`).
4. After a short delay, a new screenshot is taken and the cycle repeats until the download is confirmed (the model can also detect success text like "Download complete").
5. Fallback: if the model fails or loops, revert to standard CLI parsing.

**Model choice:**  
- **LLaVA 7B** or **BakLLaVA** quantized to 4‑bit (Q4_K_M). Size ~4.5 GB VRAM. A 3060 laptop GPU (6 GB) easily runs it.  
- Served via **Ollama** (simple `ollama pull llava:7b`). The tool communicates over its REST API.

**Prompt engineering details:**
- The prompt includes the current step context: whether we are at the main menu, search results, or download screen.
- The model is told to ignore the window decorations and focus on the terminal text.
- We maintain a short history of the last 3 actions to prevent loops (passed as part of the prompt).

**Performance:**
- Inference time ~1–3 seconds per step on an RTX 3060. A typical download sequence (search, select, start) may take 10–20 steps, so ~15–60 seconds per song for the SLM part. This is acceptable for an offline, robust solution.

**Implementation:**
- A Python class `TorlinkNavigator` that uses the Ollama API. It manages state (menu/search/result/download) and calls the model.
- If the model is unavailable or the user opts out, the tool falls back to direct `torlink` subprocess calls with parsed output.

---

### 5.5 Orchestrator & Flow Control
- Load `liked_songs.json` and a `progress.json` (to resume after interruption).
- For each song:
  1. Skip if already marked “done” in progress.
  2. Build query, launch `torlink` (or SLM navigator).
  3. Parse top result name (or capture the text via OCR if SLM mode is on).
  4. Run fuzzy verification. If fail, write to `manual_downloads.txt` and mark as “manual” in progress.
  5. If pass, download and mark “done”.
- Log every action with timestamps.
- At end, print summary: total, succeeded, failed (manual).

---

### 5.6 Post‑Processing (Optional)
- After all downloads, run a tagger using `mutagen` to set ID3 tags from the known artist/title.
- Move files to a user‑friendly folder structure (`Music/<Artist>/<Title>.mp3`).

---

## 6. Implementation Roadmap

| Step | Task |
|------|------|
| 1 | Create `bootstrap.bat` that installs Python, Node.js/npm (if missing), Ollama, ChromeDriver, pulls model, and ensures `npx torlnk` works. |
| 2 | Write `extract_liked_songs.py` with Selenium and lazy‑load scrolling. |
| 3 | Write `torlink_interactor.py` – standard subprocess module that launches `torlink` via `npx torlnk`, captures output, and does fuzzy verification. |
| 4 | Write `slm_navigator.py` – optional module that uses screenshots + local model to drive `torlink`. |
| 5 | Write `orchestrator.py` – ties extraction, interaction, and verification together. Handles resume and manual log. |
| 6 | Test on a sample library of 10–20 songs, with and without SLM mode. |
| 7 | Add a configuration file (`config.yaml`) for paths, model selection, similarity threshold, etc. |
| 8 | Final polish: progress bars (`tqdm`), error handling, retry logic for network glitches. |

---

## 7. Edge Cases & Mitigations

- **Model download fails:** The bootstrap script retries three times, then falls back to the non‑SLM mode automatically.
- **YouTube Music changes DOM:** The extraction script will use configurable CSS selectors that can be updated without touching the core logic.
- **`torlink` crashes:** The orchestrator restarts it and resumes from the last song.
- **Manual download file grows:** The user can later process it with a separate helper script that tries alternate queries or manual matching.

---

## 8. Files & Deliverables
```
project/
├── bootstrap.bat
├── config.yaml
├── requirements.txt
├── extract_liked_songs.py
├── torlink_interactor.py
├── slm_navigator.py          (optional)
├── orchestrator.py
├── utils/
│   ├── fuzzy_match.py
│   └── window_capture.py
├── liked_songs.json          (generated)
├── progress.json
├── manual_downloads.txt      (generated)
└── README.md
```
