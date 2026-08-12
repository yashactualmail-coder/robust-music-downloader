import json
import os
import subprocess
import yaml

def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open("progress.json", "w") as f:
        json.dump(progress, f, indent=4)

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    if not os.path.exists("liked_songs.json"):
        print("liked_songs.json not found. Please run extract_liked_songs.py first.")
        return

    with open("liked_songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    progress = load_progress()
    download_dir = config["app"].get("download_dir", "./downloads")
    os.makedirs(download_dir, exist_ok=True)

    for i, song in enumerate(songs):
        song_id = f"{song['artist']} - {song['title']}"
        
        if progress.get(song_id) == "done":
            print(f"Skipping {song_id} (already downloaded)")
            continue
            
        print(f"\nProcessing [{i+1}/{len(songs)}]: {song_id}")
        
        # yt-dlp search query
        query = f"{song['title']} {song['artist']} audio"
        
        # Build yt-dlp command
        # -x: extract audio
        # --audio-format flac (highest quality lossless)
        # --audio-quality 0 (best)
        # ytsearch1: returns the first search result
        cmd = [
            "yt-dlp",
            f"ytsearch1:{query}",
            "-x",
            "--audio-format", "flac",
            "--audio-quality", "0",
            "--embed-metadata",
            "-o", f"{download_dir}/%(title)s.%(ext)s"
        ]
        
        try:
            # We don't suppress output so the user can see download progress in the terminal
            subprocess.run(cmd, check=True)
            progress[song_id] = "done"
        except subprocess.CalledProcessError:
            print(f"Failed to download {song_id}")
            progress[song_id] = "failed"
            
        save_progress(progress)

    print("\nAll songs processed!")

if __name__ == "__main__":
    main()
