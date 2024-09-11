##############
# Version 3
# We dropping the image finding logic and click due to much more effecting continuous clicking.
# Create patterns based on directions & time - will unfold the dhamma pattern with enough testing
# Stuck Handle logic changed to "Experience" - most relevant here.
# #############
import random
import keyboard
import pyautogui
import time
from automation_engine import find_target_client, get_active_window_region_from_target_client

char_name = 'Lao'

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


#######################
### Script Starting ###
#######################
find_target_client(char_name)
window_region = get_active_window_region_from_target_client(char_name)
print(window_region)

find_char_center()

print("Starting AutoLvler V3...")
random_mouse_loop()

# mouse_movement_loop()
