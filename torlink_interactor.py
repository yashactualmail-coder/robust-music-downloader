import subprocess
import os
import time
from utils.fuzzy_match import verify_match

class TorlinkInteractor:
    def __init__(self, command, threshold, download_dir):
        self.command = command
        self.threshold = threshold
        self.download_dir = download_dir
        
    def download_song(self, artist, title):
        query = f"{artist} - {title}"
        print(f"Searching torlink for: {query}")
        
        # In non-SLM mode, torlink needs a way to be driven non-interactively, 
        # or we have to wrap it with pexpect/subprocess
        # Note: since torlink is interactive, a naive subprocess.run might hang
        # This is a placeholder for where the actual CLI parsing would go if torlink
        # supports non-interactive arguments (e.g., torlink search "query" --download-first)
        # Assuming torlink requires interactive input, this is why the SLM mode is useful.
        
        # Mocking the verification flow:
        # 1. Run search, capture output
        # 2. Extract first result title
        # 3. Verify match
        # 4. If match, send 'ENTER' (or equivalent download command)
        
        print("Note: Direct CLI parsing for an interactive tool is fragile.")
        print("For a robust solution on an interactive CLI, SLM mode is recommended.")
        
        # Fake match simulation for the boilerplate
        top_result = f"{artist} - {title} (320kbps)" 
        is_match = verify_match(query, top_result, self.threshold)
        
        if is_match:
            print(f"Match found ({top_result}), but Standard CLI mode is currently just a placeholder.")
            print("Please use SLM mode to actually download files.")
            return False
        else:
            print(f"No valid match found for {query}")
            return False
