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
    capture_screen_area, get_hpbar_coor, extract_hp_value, get_cq_map_coordinates

char_name = 'Lao'

# Global flags and counters
stuck_lock = threading.Lock()
script_running = True
hp_thread_running = True
hp_potion_threshold = 2777
exp_stuck = False
coords_stuck = False
stuck = False
stuck_index = 0

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


def opposite_direction(direction, random_choice=False):
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

    # If random_choice is True, pick a random direction except the current direction and its opposite
    if random_choice:
        possible_directions = [dir for dir in opposites if dir != direction and opposites[dir] != direction]
        return random.choice(possible_directions)

    # Check if the input direction is valid and return the opposite
    if direction in opposites:
        return opposites[direction]
    else:
        return "Invalid direction"


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


def wait_for(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        if check_stop():
            raise StopScriptException()
        time.sleep(0.15)  # Sleep for a short time to reduce CPU usage
    return False


def wait_for_and_handle_stuck(seconds, current_direction):
    global exp_stuck, coords_stuck, stuck_index
    """Waits for a given number of seconds, checking for exit condition."""
    if not coords_stuck:
        stuck_index = 0
    end_time = time.time() + seconds
    while time.time() < end_time:
        if check_stop():
            raise StopScriptException()
        if exp_stuck and coords_stuck:
            print(f"Character is not moving nor gaining Exp.. (exp_stuck: {exp_stuck}, coords_stuck: {coords_stuck})")
            if stuck_index == 0:
                handling_stuck_direction = opposite_direction(current_direction, False)
                print(f"(Stuck) Moving character to opposite direction: {handling_stuck_direction}")
                move_mouse_to(handling_stuck_direction)
                # Correcting the assignment
                exp_stuck = False
                coords_stuck = False
                # Wait to see if flags remain false, especially coords
                wait_for(1.3)
                stuck_index += 1
            if coords_stuck:
                handling_stuck_direction = opposite_direction(current_direction, True)
                print(f"(Stuck) Moving character to random direction: {handling_stuck_direction}")
                move_mouse_to(handling_stuck_direction)
                # Correcting the assignment
                exp_stuck = False
                coords_stuck = False
                wait_for(1.3)
                stuck_index += 1

        time.sleep(0.15)  # Sleep for a short time to reduce CPU usage
    return False


# Function to check if character is stuck
def check_coords_stuck():
    global coords_stuck, script_running
    prev_coor = None
    # print('Stuck Thread Starting...')
    time.sleep(1.1)  # Sleep at the start to give time for initial image capture
    while script_running:
        # print("Parsing stuck thread with Stuck counter = ", stuck_counter)
        time.sleep(1.2)  # Time Between Checks
        with stuck_lock:  # Acquire lock before checking
            # print("Starting stuck capture...")
            current_coor = get_cq_map_coordinates()
            # print("Parsed stuck coordinates")
            if prev_coor is not None and current_coor is not None and prev_coor == current_coor and current_coor != '':
                coords_stuck = True
                print("Character not moving, at coordinates: ", current_coor, prev_coor)
                time.sleep(2)
            else:
                prev_coor = current_coor
                coords_stuck = False


def check_exp_stuck():
    global script_running, exp_stuck, coords_stuck
    exp_stuck = False
    exp_stuck_index = 0
    previous_exp = None
    valid_experience = None
    exp_gain_tracker = []
    time.sleep(1.04)

    while script_running:
        valid_experience = None
        # print("Searching for Exp bar...")
        exp_coords = find_image(exp_bar)
        # pyautogui.moveTo(exp_coords)
        time.sleep(0.88)

        # Expanding Bar to read %
        exp_bar_region = {'top': exp_coords[1] - 8, 'left': (exp_coords[0] - 45), 'width': 230, 'height': 14}
        try:
            exp_bar_captured = capture_screen_area(exp_bar_region)
            # Extract text from the image
            extracted_text = extract_text_from_image_hp(exp_bar_captured)
            # Clean the extracted text of newlines and extra whitespace
            cleaned_text = extracted_text.replace('\n', '').replace('\r', '').strip()
            # print(f"Extracted text from Exp Bar: {cleaned_text}")

            # Validate the extracted experience value
            valid_experience = valid_exp(cleaned_text)
        except Exception as e:
            print(f"An error occurred while capturing the screen area: {e}")

        # Display the captured image
        # cv2.imshow('Captured Experience Bar', exp_bar_captured)

        if valid_experience:
            valid_experience = float(valid_experience)
            print(f"Valid Experience Value: {valid_experience}")
            exp_gain_tracker.append(valid_experience)
        else:
            print("Invalid Experience Value, restarting iteration...")
            continue  # Restart the loop iteration if the experience value is not valid

        if valid_experience == previous_exp:
            exp_stuck_index += 1
        else:
            exp_stuck_index = 0

        # Exp did not change in 2 loops (~1.5 seconds) and character didn't move
        if exp_stuck_index >= 2:
            exp_stuck = True
            print("Character is not gaining Exp..")
            time.sleep(2)

        previous_exp = valid_experience

    print(f"Exp Gain Tracker: {exp_gain_tracker}")


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
                    # print("HP: ", hp_value)
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
# Game mechanics and structure makes character movement go in rectangles of (l, 1.25*l (=L) and 1.35*l (diagonal))
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
        predominant_pattern_directions = patterns[predominant_pattern]
        other_directions = [d for d in directions if d not in predominant_pattern_directions]
    else:
        predominant_pattern_directions = []
        other_directions = directions.copy()

    # Validate & Normalize scale
    normalized_scale = float(scale / 100)
    # scale = max(0, min(normalized_scale, 1))

    # Calculate pattern total default probabilities
    predominant_pattern_total_default_prob = sum(default_probabilities[d] for d in predominant_pattern_directions)
    other_total_default_prob = sum(default_probabilities[d] for d in other_directions)

    # Step 1: Calculate total increase for predominant pattern directions
    predominant_increase = 0  # Store the total increase for predominant pattern directions
    adjusted_probabilities = {}

    print(f"\nStep 1: Adjusting probabilities for predominant pattern {predominant_pattern} "
          f"directions with scale {normalized_scale}")
    for d in directions:
        if d in predominant_pattern_directions:
            p_d_pattern = default_probabilities[d] / predominant_pattern_total_default_prob
            # Calculate the adjusted probability (limit the increase to a reasonable amount based on scale)
            adjusted_probabilities[d] = ((1 - normalized_scale) * default_probabilities[d]
                                         + normalized_scale * p_d_pattern)
            predominant_increase += (adjusted_probabilities[d] - default_probabilities[d])  # Track increase
        else:
            adjusted_probabilities[d] = default_probabilities[d]  # Initialize with default

    print(f"Adjusted probabilities: {adjusted_probabilities}")
    print(f"Total Increase for Predominant Directions: {predominant_increase}")

    # Step 2: Redistribute the increase across non-predominant directions
    if predominant_increase > 0:
        total_non_pattern_prob = sum(default_probabilities[d] for d in other_directions)
        print(f"Step 2: Redistributing the increase ({predominant_increase}) among non-predominant directions...")
        print(f"Total Probability for Non-Predominant Directions: {total_non_pattern_prob}")

        for d in other_directions:
            # Calculate the proportion of the non-predominant pattern this direction occupies
            redistribution_factor = default_probabilities[d] / total_non_pattern_prob
            redistribution_amount = min(predominant_increase, default_probabilities[d] * 0.5)  # Limit reduction
            # Subtract the redistribution amount proportionally
            adjusted_probabilities[d] -= redistribution_amount

    print(f"Step 2 Completed: Adjusted probabilities redistributed: {adjusted_probabilities}")

    # Step 3: Ensure total probability sums to 1 by adjusting any residuals
    total_adjusted_prob = sum(adjusted_probabilities.values())
    residual = 1 - total_adjusted_prob

    print(f"Step 3: Ensuring total probability sums to 1...")
    print(f"Total Adjusted Probability before residual adjustment: {total_adjusted_prob}, Residual: {residual}")

    # Distribute the residual back proportionally across all directions to make the sum exactly 1
    for d in adjusted_probabilities:
        adjusted_probabilities[d] += residual * (adjusted_probabilities[d] / total_adjusted_prob)

    print("Final Adjusted Probabilities:", adjusted_probabilities)

    return adjusted_probabilities


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

    normalized_probabilities = predominant_pattern_and_distribution(predominant_pattern, scale,
                                                                    patterns, directions, default_probabilities)

    total_directions_counter = {direction: 0 for direction in directions}

    try:
        while script_running:

            # Select the next direction based on adjusted probabilities
            current_direction = random.choices(
                population=list(normalized_probabilities.keys()),
                weights=list(normalized_probabilities.values()),
                k=1
            )[0]

            # Increment the counter for the selected direction
            total_directions_counter[current_direction] += 1

            # Remove directions to prevent double up or down movements
            ######## TBC

            if stuck:
                print("Handling stuck by moving mouse to opposite direction than what should")

            print(f"\nAI Agent Moving mouse randomly to {current_direction}")  # Move the mouse
            move_mouse_to(current_direction)
            wait_for_and_handle_stuck(13, current_direction)
            if check_stop():
                raise StopScriptException()

            previous_direction = current_direction  # Update the previous direction

    except Exception as e:
        print(f"An error occurred: {e}")

    # Print the direction counts
    print(f"Total Directions Counter: {total_directions_counter}")


# To Implement

def exp_gain_rate():
    return None


def improved_stuck():
    return None


#################
### Def Main  ###
#################

# find_char_center()def main():
print("Starting AutoLvler V3...")

# random_mouse_loop()
# mouse_movement_loop()

#######################
### Script Starting ###
#######################

if __name__ == "__main__":
    find_target_client(char_name)
    keyboard.add_hotkey('space', stop_script)  # Stop hotkey
    hp_check_thread = threading.Thread(target=check_hp_bar)
    exp_check_thread = threading.Thread(target=check_exp_stuck)
    coords_check_thread = threading.Thread(target=check_coords_stuck)
    hp_check_thread.start()
    exp_check_thread.start()
    coords_check_thread.start()

    random_mouse_loop_agent('R-L', 25)
    # random_mouse_loop()
    # main()

    hp_check_thread.join()
    exp_check_thread.join()
    coords_check_thread.join()
