import time
import json
import os
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import yaml

def extract_songs():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    profile_path = os.path.abspath(config["app"]["user_data_dir"])
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")

    print("Launching Chrome. Please log in to YouTube Music if prompted...")
    driver = uc.Chrome(options=options)
    
    driver.get("https://music.youtube.com/playlist?list=LM")
    
    input("Please log in to YouTube Music. Once you see your Liked Songs playlist, press ENTER here in the terminal to continue...")
    
    print("Scrolling to load all songs...")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Extracting songs...")
    song_elements = driver.find_elements(By.CSS_SELECTOR, "ytmusic-responsive-list-item-renderer")
    
    songs = []
    for el in song_elements:
        try:
            title_el = el.find_element(By.CSS_SELECTOR, ".title-column yt-formatted-string")
            title = title_el.text
            
            artist_el = el.find_element(By.CSS_SELECTOR, ".secondary-flex-columns yt-formatted-string a")
            artist = artist_el.text
            
            if title and artist:
                songs.append({"title": title, "artist": artist})
        except Exception:
            continue

    print(f"Extracted {len(songs)} songs.")
    
    with open("liked_songs.json", "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)
        
    driver.quit()
    print("Saved to liked_songs.json")

if __name__ == "__main__":
    extract_songs()
