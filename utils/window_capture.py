import pyautogui
import pygetwindow as gw
from PIL import Image
import base64
from io import BytesIO

def capture_screen_base64() -> str:
    """
    Captures the active window (the terminal) and returns it as a base64 encoded string.
    """
    try:
        window = gw.getActiveWindow()
        if window is not None and window.width > 0 and window.height > 0:
            region = (window.left, window.top, window.width, window.height)
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
    except Exception:
        # Fallback in case of errors
        screenshot = pyautogui.screenshot()
        
    buffered = BytesIO()
    # Save as PNG for lossless text clarity
    screenshot.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
