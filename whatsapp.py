import urllib.parse
import webbrowser
import time
import threading
import pyautogui

from parser import InvoiceParser


class WhatsAppHandler:
    @staticmethod
    def send_single(phone, text, delay, auto_press_enter, on_complete=None):
        """Runs a single send in a background thread."""
        def task():
            WhatsAppHandler.execute_send(phone, text, delay, auto_press_enter)
            if on_complete:
                on_complete()
                
        threading.Thread(target=task, daemon=True).start()
        
    @staticmethod
    def execute_send(phone, text, delay, auto_press_enter):
        """The core synchronous logic to open WA and, optionally, press Enter."""
        # Defense-in-depth: never auto-press Enter for a number that doesn't
        # look like a valid Indonesian mobile number, even if bad data made
        # it this far. Worst case here is just an extra manual click.
        if phone and not InvoiceParser.is_valid_indonesian_phone(phone):
            phone = ""

        if phone:
            url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(text)}"
        else:
            url = f"whatsapp://send?text={urllib.parse.quote(text)}"
            
        webbrowser.open(url)
        
        # Only auto-press Enter if a phone number exists AND the user has
        # explicitly opted into auto-send. This is an uncontrolled global
        # keystroke, so it stays opt-in rather than the default behavior.
        if phone and auto_press_enter:
            time.sleep(delay)
            pyautogui.press('enter')
            time.sleep(0.5) # Brief buffer after pressing enter