import pyautogui
import time
import keyboard
import pygetwindow as gw


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


def run_autogui_script(click_interval, script_duration, user_ctrl):
    print("\nAuto-clicker script started. Press Ctrl+S to stop.")
    time.sleep(1)
    start_time = time.time()
    # Defining click counter to be used in XP Skill key press
    click_counter = 0
    try:
        # keyboard.press('ctrl')

        while True:

            if user_ctrl == 'Y':
                keyboard.press('ctrl')

            if time.time() - start_time > script_duration:
                print("Run duration exceeded. Stopping script.\n Hope you had a good hunt!")
                break

            if keyboard.is_pressed('ctrl+s'):
                print("Script stopped by Ctrl+S.")
                break

            if is_window_active(WINDOW_TITLES):
                if click_counter % 25 == 0:
                    print('\nXP skill triggered')
                    keyboard.release('ctrl')
                    for i in range(7):
                        keyboard.press_and_release('F10')
                    keyboard.press_and_release('F10')
                    if user_ctrl == 'Y':
                        keyboard.press('ctrl')

                pyautogui.click()
                pyautogui.rightClick()
                click_counter += 1
                time.sleep(click_interval)
            else:
                print("Defined Game window is not active. Please Alt-Tab into one of the defined Character"
                      "\nWaiting...")
                keyboard.release('ctrl')
                time.sleep(3)  # Wait for 3 seconds before checking again

    except Exception as e:
        print(f"Script stopped due to an error: {e}")
    finally:
        keyboard.release('ctrl')


def get_click_interval():
    while True:
        try:
            seconds = input("\nPlease enter click interval (time between clicks) or leave blank for default: ")
            if seconds == "":
                return None
            seconds = float(seconds)
            return seconds
        except ValueError:
            print("Invalid input. Please enter a valid decimal value or leave blank.")


def get_script_duration():
    while True:
        user_input = input(
            "Please enter the duration for the script to run or leave blank for default: ")
        if user_input == "":
            return None
        try:
            duration = float(user_input)
            return duration
        except ValueError:
            print("Invalid input. Please enter a valid decimal value or leave blank.")


if __name__ == "__main__":
    print("Good Morning PonPon,\nGood luck in your hunting today!\n")
    char_names = input("Enter the characters you will be using today, separated by a semicolon (;): ")
    char_name_list = char_names.split(';')
    WINDOW_TITLES = [f"{char_name.strip()} - X" for char_name in char_name_list]
    print(f"Defined Windows: {WINDOW_TITLES}")

    user_click_interval = get_click_interval()
    if user_click_interval is None:
        user_click_interval = 0.32
    user_script_duration = get_script_duration()
    if user_script_duration is None:
        user_script_duration = 99999
    user_ctrl_choice = input("\nHold Down Ctrl? (Y=Yes) (N=No): ")
    run_autogui_script(user_click_interval, user_script_duration, user_ctrl_choice)
