import time
import keyboard
import pygetwindow as gw
from automation_engine import find_target_client

char_name = 'Lao'


def run_autofly_script():
    print("Auto-Fly started. Press Ctrl+S to stop.")
    time.sleep(2)
    start_time = time.time()

    while True:
        for i in range(9):
            keyboard.press_and_release('F10')
            time.sleep(0.07)
        time.sleep(7)

        if keyboard.is_pressed('ctrl+s'):
            print("Script stopped by Ctrl+S.")
            break


if __name__ == "__main__":
    find_target_client(char_name)
    run_autofly_script()
