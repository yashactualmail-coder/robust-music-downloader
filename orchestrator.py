import sys
import yaml
import json
import os
import subprocess
from torlink_interactor import TorlinkInteractor
from slm_navigator import SLMNavigator

def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open("progress.json", "w") as f:
        json.dump(progress, f, indent=4)

def log_manual(song, reason):
    with open("manual_downloads.txt", "a", encoding="utf-8") as f:
        f.write(f"{song['artist']} - {song['title']} | Reason: {reason}\n")

def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    if not os.path.exists("liked_songs.json"):
        print("liked_songs.json not found. Please run extract_liked_songs.py first.")
        return

    with open("liked_songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    progress = load_progress()
    
    use_slm = config["app"].get("use_slm", False) or "--slm" in sys.argv
    threshold = config["app"].get("similarity_threshold", 80)
    download_dir = config["app"].get("download_dir", "./downloads")
    
    os.makedirs(download_dir, exist_ok=True)

    if use_slm:
        print("Using SLM mode for navigation.")
        navigator = SLMNavigator(config["slm"]["api_url"], config["slm"]["model_name"])
    else:
        print("Using standard CLI interaction.")
        interactor = TorlinkInteractor(config["torlink"]["command"], threshold, download_dir)

    for i, song in enumerate(songs):
        song_id = f"{song['artist']} - {song['title']}"
        
        if progress.get(song_id) == "done":
            print(f"Skipping {song_id} (already downloaded)")
            continue
        if progress.get(song_id) == "manual":
            print(f"Skipping {song_id} (marked for manual download)")
            continue
            
        print(f"\nProcessing [{i+1}/{len(songs)}]: {song_id}")
        
        success = False
        if use_slm:
            process = subprocess.Popen(config["torlink"]["command"], shell=True)
            import time
            time.sleep(5) # wait for startup
            
            success = navigator.download_song(song['artist'], song['title'])
            
            process.terminate()
        else:
            success = interactor.download_song(song['artist'], song['title'])

        if success:
            progress[song_id] = "done"
        else:
            progress[song_id] = "manual"
            log_manual(song, "Failed or verification mismatch")

        save_progress(progress)

    print("\nAll songs processed!")

if __name__ == "__main__":
    main()
