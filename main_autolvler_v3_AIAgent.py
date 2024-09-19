##############
# Version 3
# We dropping the image finding logic and click due to much more effecting continuous clicking.
# Create patterns based on directions & time - will unfold the dhamma pattern with enough testing
# Stuck Handle logic changed to "Experience" - most relevant here.
# #############
import random
import re
import threading
import keyboard
import pyautogui
import time
import os

from X_Assistant.image_processing_engine import extract_text_from_image_hp
from automation_engine import find_target_client, find_image, \
    capture_screen_area, get_hpbar_coor, extract_hp_value

char_name = 'Lao'

script_running = True
hp_thread_running = True
hp_potion_threshold = 2777
stuck = False
exp_stuck_index = 0

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


class StopScriptException(Exception):
    pass


def find_char_center():
    screen_center_x, screen_center_y = pyautogui.size()
    screen_center = (screen_center_x // 2, screen_center_y // 2)
    print("Screen Center:", screen_center)

    # Create character center
    char_center = (screen_center[0], screen_center[1] + 11)  # Be Aware of X-Y Offset and Y changing

    print("Char Center:", char_center)


def move_mouse_to(coords_name):
    """Moves the mouse to the specified coordinates."""
    x, y = coords[coords_name]
    pyautogui.moveTo(x, y)


def opposite_direction(direction):
    # Define a dictionary mapping each direction to its opposite
    opposites = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left',
        'up_left': 'down_right',
        'up_right': 'down_left',
        'down_left': 'up_right',
        'down_right': 'up_left'
    }

    # Check if the input direction is valid and return the opposite
    if direction in opposites:
        return opposites[direction]
    else:
        return "Invalid direction"


def wait_for_and_handle_stuck(seconds, current_direction):
    global stuck, exp_stuck_index
    """Waits for a given number of seconds, checking for exit condition."""
    end_time = time.time() + seconds
    while time.time() < end_time:
        if check_stop():
            raise StopScriptException()
        if stuck:
            handling_stuck_direction = opposite_direction(current_direction)
            move_mouse_to(handling_stuck_direction)
            stuck = False
            # Give time to get un-stuck
            exp_stuck_index = 0
            wait_for_and_handle_stuck(2.5, handling_stuck_direction)
            # time.sleep(1)

        time.sleep(0.15)  # Sleep for a short time to reduce CPU usage
    return False


def stop_script():
    """Set the script_running flag to False to stop the script."""
    global script_running
    script_running = False


def check_stop():
    global script_running

    if not script_running:
        print("Stopping Script from check_stop function call in main engine")
        raise StopScriptException()  # Raise custom exception to stop the script

    return False  # Continue script_running


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


def check_exp_stuck():
    global script_running, stuck, exp_stuck_index
    stuck = False
    exp_stuck_index = 0
    previous_exp = None
    time.sleep(2)

    while script_running:
        # print("Searching for Exp bar...")
        exp_coords = find_image(exp_bar)
        # pyautogui.moveTo(exp_coords)
        time.sleep(1.2)

        # Expanding Bar to read %
        exp_bar_region = {'top': exp_coords[1] - 8, 'left': (exp_coords[0] - 45), 'width': 230, 'height': 14}
        try:
            exp_bar_captured = capture_screen_area(exp_bar_region)
        except Exception as e:
            print(f"An error occurred while capturing the screen area: {e}")

        # Display the captured image
        # cv2.imshow('Captured Experience Bar', exp_bar_captured)

        # Extract text from the image
        extracted_text = extract_text_from_image_hp(exp_bar_captured)
        # Clean the extracted text of newlines and extra whitespace
        cleaned_text = extracted_text.replace('\n', '').replace('\r', '').strip()
        # print(f"Extracted text from Exp Bar: {cleaned_text}")

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
            stuck = True
            print("Character is stuck and not gaining Exp")
            time.sleep(3)

        previous_exp = valid_experience


def check_hp_bar():
    global hp_potion_threshold, script_running, hp_thread_running
    time.sleep(2)
    print('Hp Bar Thread Starting..')
    previous_valid_hp = None
    while script_running:
        while script_running and hp_thread_running:  # Keep checking HP as long as the script is running
            try:
                hp_bar = get_hpbar_coor()
                hp_img = capture_screen_area(hp_bar)
                extracted_text = extract_text_from_image_hp(hp_img)
                hp_value = extract_hp_value(extracted_text)
                if hp_value is not None:
                    print("HP: ", hp_value)
                    previous_valid_hp = hp_value
                    if hp_value < hp_potion_threshold:
                        keyboard.press_and_release('f1')
                # Treating Scenario in which hp drops critically low that image is not recognized
                if hp_value is None and previous_valid_hp is not None:
                    keyboard.press_and_release('f1')
                    previous_valid_hp = None
            except Exception as e:
                print(f"An error occurred during HP Thread: {e}")
            time.sleep(1.2)
        # Sleep while auto-leveler is not working
        time.sleep(1)


def mouse_movement_loop():
    global stuck, script_running
    """Main loop to move the mouse and listen for the space key press."""
    try:
        while script_running:
            # Move in L-U-R-D pattern
            for direction in ['right', 'down', 'left', 'up']:
                print(f"Moving mouse to {direction}")
                move_mouse_to(direction)
                wait_for_and_handle_stuck(12, direction)
                if check_stop():
                    raise StopScriptException()
            # Move in UL-R-DL-L pattern
            for direction in ['down_right', 'up_left']:
                print(f"Moving mouse to {direction}")
                move_mouse_to(direction)
                wait_for_and_handle_stuck(17, direction)
                if check_stop():
                    raise StopScriptException()
    except Exception as e:
        print(f"An error occurred: {e}")


def random_mouse_loop():
    global stuck, script_running
    """Randomly moves the mouse to one of the coords while preventing double up-related or down-related movements."""
    previous_direction = None

    try:
        while script_running:
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
            wait_for_and_handle_stuck(10, current_direction)
            if check_stop():
                raise StopScriptException()
            if check_stop():  # Check for exit condition
                return

            previous_direction = current_direction  # Update the previous direction

    except Exception as e:
        print(f"An error occurred: {e}")


######################################################################################################################
# Introducing: AI Agent for random mouse movement with Knowledge Base of Game mechanics.
# Game mechanics and structure makes character movement go in rectangulars of (l, 1.25*l (=L) and 1.35*l (diagonal))
# Map is also defined as a rectangular of same size ratios.
# Therefore, the default distribution is wrong if approached equally - as characters moves at a faster unit
# speed when clicking up then when clicking left/right/ur/dl/ur/dr.
# That is because if we presume 10s moving in each direction, the up scare would have covered
# more units than other patterns in the same unit of time.
# To ensure balance and allow Model to choose predominance based on circumstances,
# We are going to use Normalized Distribution and add on top of that the scaled predominant pattern.
######################################################################################################################

def predominant_pattern_and_distribution(predominant_pattern, scale, patterns, directions, default_probabilities):
    if predominant_pattern in patterns:
        pattern_directions = patterns[predominant_pattern]
        other_directions = [d for d in directions if d not in pattern_directions]
    else:
        pattern_directions = []
        other_directions = directions.copy()

    # Calculate pattern total default probabilities
    pattern_total_default_prob = sum(default_probabilities[d] for d in pattern_directions)
    other_total_default_prob = sum(default_probabilities[d] for d in other_directions)

    adjusted_probabilities = {}
    for d in directions:
        if scale == 0 or not pattern_directions:
            # Use default probabilities
            adjusted_probabilities[d] = default_probabilities[d]
        else:
            if d in pattern_directions:
                # Adjusted probability for pattern directions
                p_d_pattern = (default_probabilities[d] / pattern_total_default_prob) * 0.8
            else:
                # Adjusted probability for other directions
                p_d_pattern = (default_probabilities[d] / other_total_default_prob) * 0.2
            # Linear interpolation
            adjusted_probabilities[d] = (1 - scale) * default_probabilities[d] + scale * p_d_pattern

    print(f"Adjusted Probabilities distribution based on predominant pattern {predominant_pattern} "
          f"and scale {scale}")
    print(adjusted_probabilities)

    # Normalize probabilities after removal
    total_prob = sum(adjusted_probabilities.values())
    normalized_probabilities = {d: p / total_prob for d, p in adjusted_probabilities.items()}
    return normalized_probabilities


def random_mouse_loop_agent(predominant_pattern=None, scale=0):
    global stuck, script_running, coords
    """Randomly moves the mouse to one of the coords while preventing double up-related or down-related movements.

    Args:
        predominant_pattern (str): The predominant movement pattern. Can be None, 'U-D', 'R-L', 'UL-DR', 'UR-DL'.
        scale (float): Scale from 0 to 1 indicating the influence towards the predominant pattern.
    """
    previous_direction = None

    # Define patterns
    patterns = {
        'U-D': ['up', 'down'],
        'R-L': ['left', 'right'],
        'UL-DR': ['up-left', 'down-right'],
        'UR-DL': ['up-right', 'down-left']
    }

    # All possible directions
    directions = list(coords.keys())

    # Relative speeds (higher means faster) due to Game mechanics (Character and Maps knowledge base)
    # Higher-Speed = character will finish a full map run on target direction faster
    # Therefore, the probability distribution for balanced movement must be inversed to Speed
    speeds = {
        'up': 1.0,  # Fastest
        'down': 1.0,  # Fastest
        'left': 0.8,
        'right': 0.8,
        'up_left': 0.74,
        'up_right': 0.74,
        'down_left': 0.74,
        'down_right': 0.74
    }

    # Calculate default probabilities inversely proportional to speeds
    inverse_speeds = {d: 1.0 / speeds[d] for d in directions}
    total_inverse_speed = sum(inverse_speeds.values())
    default_probabilities = {d: inverse_speeds[d] / total_inverse_speed for d in directions}

    print(f"Default Probabilities for Char movement: f{default_probabilities})")

    # Validate scale
    scale = max(0, min(scale, 1))  # Ensure scale is between 0 and 1

    normalized_probabilities = predominant_pattern_and_distribution(predominant_pattern, scale,
                                                                    patterns, directions, default_probabilities)

    try:
        while script_running:

            # Select the next direction based on adjusted probabilities
            current_direction = random.choices(
                population=list(normalized_probabilities.keys()),
                weights=list(normalized_probabilities.values()),
                k=1
            )[0]

            # Remove directions to prevent double up or down movements
            ######## TBC

            if stuck:
                print("Handling stuck by moving mouse to opposite direction than what should")

            print(f"\nAI Agent Moving mouse randomly to {current_direction}")  # Move the mouse
            move_mouse_to(current_direction)
            wait_for_and_handle_stuck(10, current_direction)
            if check_stop():
                raise StopScriptException()

            previous_direction = current_direction  # Update the previous direction

    except Exception as e:
        print(f"An error occurred: {e}")


def exp_gain_rate():
    return None


#################
### Def Main  ###
#################

# find_char_center()def main():
print("Starting AutoLvler V3...")

# random_mouse_loop()
mouse_movement_loop()

#######################
### Script Starting ###
#######################

if __name__ == "__main__":
    find_target_client(char_name)
    keyboard.add_hotkey('space', stop_script)  # Stop hotkey
    hp_check_thread = threading.Thread(target=check_hp_bar)
    exp_check_thread = threading.Thread(target=check_exp_stuck)
    hp_check_thread.start()
    exp_check_thread.start()

    random_mouse_loop_agent()
    # random_mouse_loop()
    # main()

    hp_check_thread.join()
    exp_check_thread.join()
