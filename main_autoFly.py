import time
import keyboard
import pygetwindow as gw

# Duration for which the script runs (in seconds)
RUN_DURATION = 10000
# List of window titles
WINDOW_TITLES = ["Lao - ", "BeWater - "]


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


def run_autogui_script():
    print("Auto-Fly started. Press Ctrl+S to stop.")
    time.sleep(2)
    start_time = time.time()
    try:
        # keyboard.press('ctrl')

        while True:
            # keyboard.press('ctrl')

            if time.time() - start_time > RUN_DURATION:
                print("Run duration exceeded. Stopping script.")
                break

            if keyboard.is_pressed('ctrl+s'):
                print("Script stopped by Ctrl+S.")
                break

            if is_window_active(WINDOW_TITLES):
                time.sleep(0.5)
                for i in range(7):
                    keyboard.press_and_release('F8')
                time.sleep(7)
                print("Enjoy your Flight!")

            else:
                print("Defined window is not active. Waiting...")
                keyboard.release('ctrl')
                time.sleep(1)  # Wait for 1 second before checking again

    except Exception as e:
        print(f"Script stopped due to an error: {e}")


if __name__ == "__main__":
    run_autogui_script()
