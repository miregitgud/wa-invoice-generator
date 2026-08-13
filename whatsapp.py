import urllib.parse
import webbrowser
import time
import threading
import pyautogui

class WhatsAppHandler:
    @staticmethod
    def send_single(phone, text, delay, on_complete=None):
        """Runs a single send in a background thread."""
        def task():
            WhatsAppHandler.execute_send(phone, text, delay)
            if on_complete:
                on_complete()
                
        threading.Thread(target=task, daemon=True).start()
        
    @staticmethod
    def execute_send(phone, text, delay):
        """The core synchronous logic to open WA and press Enter."""
        if phone:
            url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(text)}"
        else:
            url = f"whatsapp://send?text={urllib.parse.quote(text)}"
            
        webbrowser.open(url)
        
        # Only auto-press Enter if a phone number exists
        if phone:
            time.sleep(delay)
            pyautogui.press('enter')
            time.sleep(0.5) # Brief buffer after pressing enter