import requests
import json
import time
import pyautogui
from utils.window_capture import capture_screen_base64

class SLMNavigator:
    def __init__(self, api_url, model_name):
        self.api_url = api_url
        self.model_name = model_name
        self.history = []

    def decide_next_action(self, artist, title):
        img_base64 = capture_screen_base64()
        
        prompt = f"""
        You are controlling the CLI tool `torlink`. The current screen is shown.
        We want to search for: "{artist} - {title}" and download the first result.
        What single key should be pressed next? (UP, DOWN, ENTER, TAB, ESC, q)
        If you need to type the search query, reply with the exact text to type prefixed by "TYPE:".
        If the download is complete, reply with "DONE".
        Respond with only the key name, TYPE command, or DONE.
        History of last actions: {self.history[-3:]}
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "images": [img_base64]
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            action = response.json().get("response", "").strip()
            return action
        except Exception as e:
            print(f"SLM Error: {e}")
            return "ERROR"

    def execute_action(self, action):
        print(f"SLM decided action: {action}")
        self.history.append(action)
        
        if action.startswith("TYPE:"):
            text = action.replace("TYPE:", "").strip()
            pyautogui.write(text)
            pyautogui.press('enter')
        elif action in ["UP", "DOWN", "ENTER", "TAB", "ESC", "q"]:
            pyautogui.press(action.lower())
        elif action == "DONE":
            return True
        else:
            print(f"Unknown action: {action}")
            
        return False
        
    def download_song(self, artist, title):
        print(f"Starting SLM navigation for {artist} - {title}")
        # Assuming torlink is already open in the active window
        max_steps = 20
        steps = 0
        
        while steps < max_steps:
            action = self.decide_next_action(artist, title)
            if action == "ERROR":
                return False
                
            is_done = self.execute_action(action)
            if is_done:
                print("SLM reported download complete.")
                return True
                
            time.sleep(2) # Wait for UI to update
            steps += 1
            
        print("SLM navigation timed out.")
        return False
