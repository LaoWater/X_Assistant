import pyautogui
import time
import keyboard
import threading
from pynput import mouse
import pygetwindow as gw

# Duration for which the script runs (in seconds)
RUN_DURATION = 10000
WINDOW_TITLES = ["Lao - ", "TheHunt(er) - ", "BeWater - "]


class ClickListener:
    def __init__(self):
        self.last_click_time = None
        self.listener = mouse.Listener(on_click=self.on_click)

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            current_time = time.time()
            if self.last_click_time:
                time_diff = current_time - self.last_click_time
                print(f"Time between clicks: {time_diff} seconds")
            self.last_click_time = current_time

    def run(self):
        with self.listener:
            self.listener.join()

    def stop(self):
        self.listener.stop()


def is_window_active(titles):
    for title in titles:
        try:
            window = gw.getWindowsWithTitle(title)[0]  # Get the first window with the given title
            if window.isActive:
                return True
        except IndexError:
            # Window with the specified title not found, continue checking next title
            continue
    return False


def run_autogui_script(user_input_time):
    print("Auto-clicker script started. Press Ctrl+S to stop.")
    time.sleep(2)
    start_time = time.time()
    user_input_time = 0.01
    try:
        # keyboard.press('ctrl')

        while True:
            keyboard.press('ctrl')

            if time.time() - start_time > RUN_DURATION:
                print("Run duration exceeded. Stopping script.")
                break

            if keyboard.is_pressed('ctrl+s'):
                print("Script stopped by Ctrl+S.")
                break

            if is_window_active(WINDOW_TITLES):
                pyautogui.click()
                pyautogui.rightClick()
                time.sleep(user_input_time)
            else:
                print("Defined window is not active. Waiting...")
                keyboard.release('ctrl')
                time.sleep(1)  # Wait for 1 second before checking again

    except Exception as e:
        print(f"Script stopped due to an error: {e}")
    finally:
        keyboard.release('ctrl')
        click_listener.stop()  # Explicitly stop the click listener


def get_seconds():
    while True:
        try:
            seconds = float(input("Please enter a decimal value representing seconds: "))
            return seconds
        except ValueError:
            print("Invalid input. Please enter a valid decimal value.")


if __name__ == "__main__":
    # user_input_time = get_seconds()
    click_listener = ClickListener()
    listener_thread = threading.Thread(target=click_listener.run)
    listener_thread.start()

    run_autogui_script(0.1)

    listener_thread.join()
