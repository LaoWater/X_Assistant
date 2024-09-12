##############
# Version 3
# We dropping the image finding logic and click due to much more effecting continuous clicking.
# Create patterns based on directions & time - will unfold the dhamma pattern with enough testing
# Stuck Handle logic changed to "Experience" - most relevant here.
# #############
import random
import re

import cv2
import keyboard
import pyautogui
import time
import os

from X_Assistant.image_processing_engine import extract_text_from_image_hp
from automation_engine import find_target_client, get_active_window_region_from_target_client, find_image, \
    capture_screen_area, get_hpbar_coor, extract_hp_value

char_name = 'PonPon'

script_running = True
hp_thread_running = True
hp_potion_threshold = 1500

# Define pixel coordinates
coords = {
    'left': (911, 551),
    'up_left': (911, 519),
    'up_right': (1005, 513),
    'right': (1013, 551),
    'up': (960, 528),
    'down': (960, 576),
    'down_left': (916, 559),
    'down_right': (990, 573)
}

# Define sets of up-related and down-related directions
up_related = {'up', 'up_left', 'up_right'}
down_related = {'down', 'down_left', 'down_right'}

# Using Experience Bar for Stuck() Logic - If experience is un-changed for 4+ seconds -> Stuck
current_directory = os.getcwd()
# Construct the path to the ExperienceBar.png file
exp_bar = os.path.join(current_directory, "Auto_Lvler_Images", "V2 - Prestige", "ExperienceBar.png")


def find_char_center():
    screen_center_x, screen_center_y = pyautogui.size()
    screen_center = (screen_center_x // 2, screen_center_y // 2)
    print("Screen Center:", screen_center)

    # Create character center
    char_center = (screen_center[0], screen_center[1] + 11)  # Be Aware of X-Y Offset and Y changing
    char_center_x = char_center[0]
    char_center_y = char_center[1]

    print("Char Center:", char_center)


def move_mouse_to(coords_name):
    """Moves the mouse to the specified coordinates."""
    x, y = coords[coords_name]
    pyautogui.moveTo(x, y)


def mouse_movement_loop():
    """Main loop to move the mouse and listen for the space key press."""
    try:
        while True:
            # Move in L-U-R-D pattern
            for direction in ['right', 'down', 'left', 'up']:
                print(f"\nMoving mouse to {direction}")
                move_mouse_to(direction)
                time.sleep(15)
                if check_for_exit():
                    return
            # Move in UL-R-DL-L pattern
            for direction in ['down_right', 'up_left']:
                print(f"\nMoving mouse to {direction}")
                move_mouse_to(direction)
                time.sleep(18)
                if check_for_exit():
                    return
    except Exception as e:
        print(f"An error occurred: {e}")


def wait_for(seconds):
    """Waits for a given number of seconds, checking for exit condition."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        if keyboard.is_pressed('space'):
            print("Space pressed, stopping the loop.")
            return True
        time.sleep(0.1)  # Sleep for a short time to reduce CPU usage
    return False


def check_for_exit():
    """Checks if the space key has been pressed to exit the loop."""
    if keyboard.is_pressed('space'):
        print("Space pressed, stopping the loop.")
        return True
    return False


def random_mouse_loop():
    """Randomly moves the mouse to one of the coords while preventing double up-related or down-related movements."""
    previous_direction = None

    try:
        while True:
            current_direction = random.choice(list(coords.keys()))  # Randomly select a direction

            # Prevent double up-related or down-related movements
            if previous_direction in up_related:
                while current_direction in up_related:
                    current_direction = random.choice(list(coords.keys()))
            elif previous_direction in down_related:
                while current_direction in down_related:
                    current_direction = random.choice(list(coords.keys()))

            print(f"\nMoving mouse randomly to {current_direction}")  # Move the mouse
            move_mouse_to(current_direction)
            time.sleep(3)  # Stay in the current position for 3 seconds

            if check_for_exit():  # Check for exit condition
                return

            previous_direction = current_direction  # Update the previous direction

    except Exception as e:
        print(f"An error occurred: {e}")


def valid_exp(text):
    """
    Extracts and validates the experience value from the given text.
    Returns the extracted value if it is in the format UU.DDD, otherwise returns None.
    """
    # Regular expression pattern to match the format UU.DDD
    pattern = r'(\d{1,2}\.\d{3})'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Return the matched value if it matches the desired format
        return match.group(0)
    else:
        # No valid value found
        return None


def check_exp():
    global script_running
    stuck = False
    exp_stuck_index = 0
    previous_exp = None

    while script_running:
        print("Searching for Exp bar..")
        exp_coords = find_image(exp_bar)
        # pyautogui.moveTo(exp_coords)
        time.sleep(1.2)

        # Expanding Bar to read %
        exp_bar_region = {'top': exp_coords[1] - 8, 'left': (exp_coords[0] - 45), 'width': 230, 'height': 14}
        exp_bar_captured = capture_screen_area(exp_bar_region)

        # Display the captured image
        # cv2.imshow('Captured Experience Bar', exp_bar_captured)

        # Extract text from the image
        extracted_text = extract_text_from_image_hp(exp_bar_captured)
        # Clean the extracted text of newlines and extra whitespace
        cleaned_text = extracted_text.replace('\n', '').replace('\r', '').strip()
        print(f"Extracted text from Exp Bar: {cleaned_text}")

        # Validate the extracted experience value
        valid_experience = valid_exp(cleaned_text)

        if valid_experience:
            print(f"Valid Experience Value: {valid_experience}")
        else:
            print("Invalid Experience Value, restarting iteration...")
            continue  # Restart the loop iteration if the experience value is not valid

        if valid_experience == previous_exp:
            exp_stuck_index += 1
        else:
            exp_stuck_index = 0

        # Exp did not change in 3 loops (~4 seconds)
        if exp_stuck_index >= 3:
            print("Character is stuck and not gaining Exp")

        previous_exp = valid_experience


def check_hp_bar():
    global hp_potion_threshold, script_running, hp_thread_running
    time.sleep(2)
    print('Hp Bar Thread Starting..')
    while script_running:
        while script_running and hp_thread_running:  # Keep checking HP as long as the script is running
            try:
                hp_bar = get_hpbar_coor()
                hp_img = capture_screen_area(hp_bar)
                extracted_text = extract_text_from_image_hp(hp_img)
                hp_value = extract_hp_value(extracted_text)
                if hp_value is not None:
                    print("HP: ", hp_value)
                    if hp_value < hp_potion_threshold:
                        keyboard.press_and_release('f1')
            except Exception as e:
                print(f"An error occurred during HP Thread: {e}")
            time.sleep(1.2)
        # Sleep while auto-leveler is not working
        time.sleep(1)


#######################
### Script Starting ###
#######################
find_target_client(char_name)
window_region = get_active_window_region_from_target_client(char_name)
print(window_region)

find_char_center()

print("Starting AutoLvler V3...")
# random_mouse_loop()
# mouse_movement_loop()

check_exp()

# check_hp_bar()
