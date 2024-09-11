from datetime import datetime
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import time
import pyautogui

# Mouse and keyboard controllers
mouse = MouseController()
keyboard = KeyboardController()
last_click_time = None

# Flag to control the execution of threads
running = True


# Function to perform right click every 3 seconds
def right_click_task():
    global running
    while running:
        # Mouse.click avg time per click: 0.002
        # mouse.click(Button.right, 1)
        # Pyautogui avg time per click: 0.203 (100x more processing time LOL)
        pyautogui.rightClick()
        # time.sleep(1.03)


# Function to press F3 every 5 seconds
def press_f3_task():
    global running
    while running:
        keyboard.press(Key.f3)
        keyboard.release(Key.f3)
        time.sleep(5)


def on_click(x, y, button, pressed):
    global last_click_time
    if button == Button.right and pressed:
        current_time = datetime.now()
        if last_click_time:
            elapsed_time = current_time - last_click_time
            print(f"Time between right clicks: {elapsed_time}")
        else:
            print("Right click detected")
        last_click_time = current_time


def on_press(key):
    global running
    if key == Key.space:
        print("Space key pressed, stopping...")
        running = False
        return False  # Return False to stop the listener


# Setting up and starting the mouse listener thread
def start_listeners():
    mouse_listener = MouseListener(on_click=on_click)
    keyboard_listener = KeyboardListener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()

    keyboard_listener.join()  # Wait for the keyboard listener to stop
    mouse_listener.stop()  # Manually stop the mouse listener


# Main function to start all tasks
def main():
    time.sleep(2)
    threading.Thread(target=right_click_task, daemon=True).start()
    # threading.Thread(target=press_f3_task, daemon=True).start()

    # Starting the listeners
    start_listeners()


if __name__ == "__main__":
    main()
