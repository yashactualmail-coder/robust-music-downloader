import pyautogui
from PIL import Image
import base64
from io import BytesIO

def capture_screen_base64() -> str:
    """
    Captures the primary screen and returns it as a base64 encoded string.
    """
    screenshot = pyautogui.screenshot()
    buffered = BytesIO()
    # Compress a bit and save as JPEG
    screenshot.convert("RGB").save(buffered, format="JPEG", quality=70)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
