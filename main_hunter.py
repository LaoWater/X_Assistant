# ----------------------------------------------------------------------------------------------
# The Hunter
#
# This tool is an image-processing hunting-bot for CQ online.
#
# Author :  Neo
# ----------------------------------------------------------------------------------------------


import time
import pyautogui
import keyboard
import threading
import random
import winsound
from automation_engine import capture_screen_area, \
    get_hpbar_coor, find_and_click_chat_button, \
    get_system_chat_coordinates, is_coordinates_valid, get_cq_map_coordinates, find_target_client, validate_chat
from image_processing_engine import extract_text_from_image_hp, extract_text_from_image


# Define the Pattern class
class HuntingPattern:
    def __init__(self, number, name, shape, start_point, start_direction, limit_1, limit_2,
                 limit_3, limit_4, step_size):
        self.number = number
        self.name = name
        self.shape = shape
        self.start_point = start_point
        self.start_direction = start_direction
        self.limit_1 = limit_1
        self.limit_2 = limit_2
        self.limit_3 = limit_3
        self.limit_4 = limit_4
        self.step_size = step_size


# Global flags and counters
stuck_lock = threading.Lock()
script_running = True
script_paused = False
stuck = False
hp_bar_changed = False
counter_1, counter_2, counter_3, counter_4 = 0, 0, 0, 0
stuck_counter = 0
prev_coor = ''
loot_counter = 0

# Customizable Loot stopping words
hp_threshold = 2000

# Duration for which the script should run (in seconds)
run_duration = 3600  # Adjust this value to your desired duration

char_name = 'Lao'

# Customizable Loot stopping words
search_words = ['Ring', 'DragonBall', 'Necklace', 'Super', 'Boots', 'Bow', 'SuperDragonBall', 'Bag']  # Loot

# Define patterns
pattern_0 = HuntingPattern(0, "DesertCity", "rectangular", "DL", "Up",
                           80, 52, 80, 51, 10)

pattern_1 = HuntingPattern(1, "BI", "rectangular", "DL", "Up",
                           15, 12, 15, 12, 7)

pattern_2 = HuntingPattern(1, "BI2", "rectangular", "DL", "Up",
                           3, 12, 3, 12, 7)

current_hunting_pattern = pattern_0

# Cyclone Adjustment
cyclone_adjustment = 1


def find_pattern_limits():
    return 1


def find_pattern_steps(shape, start_point, start_direction, step_size):
    # Currently configured for Resolution: resize_and_center_window("Name - ", 1650, 920)
    # Get center coordinates of the screen
    screen_center_x, screen_center_y = pyautogui.size()
    screen_center = (screen_center_x // 2, screen_center_y // 2)
    print("Screen Center:", screen_center)

    # Create character center
    char_center = (screen_center[0], screen_center[1] + 11)  # Be Aware of X-Y Offset and Y changing
    char_center_x = char_center[0]
    char_center_y = char_center[1]

    print("Char Center:", char_center)

    # Define Step Size - Originally created on Mother 1920x1080 27'
    # * PPI dependent
    step_increment_UD = 32
    step_increment_LR = 61
    # Non-PPI dependent
    step_increase_UD = step_increment_UD * step_size
    step_increment_LR = round(step_increment_LR * (step_size / 1.5))

    next_step_up = (char_center_x, char_center_y - step_increase_UD)
    next_step_right = (char_center_x + step_increment_LR, char_center_y)
    # Adjusting Down path to allow perfect scatter of step 9 without hitting the XP bar
    next_step_down = (char_center_x, char_center_y + step_increase_UD)
    next_step_left = (char_center_x - step_increment_LR, char_center_y)
    next_step_1, next_step_2, next_step_3, next_step_4 = 0, 0, 0, 0

    if shape == 'rectangular':
        if start_point == 'DL':
            if start_direction == 'Up':
                next_step_1 = next_step_up
                next_step_2 = next_step_right
                next_step_3 = next_step_down
                next_step_4 = next_step_left

    return next_step_1, next_step_2, next_step_3, next_step_4


def hunting_engine():
    global script_running, script_paused, stuck
    global counter_1, counter_2, counter_3, counter_4, stuck_counter, \
        pattern_next_steps, current_hunting_pattern

    start_time = time.time()  # Record the start time
    next_steps = pattern_next_steps
    print("Calculated Pattern steps:\n", next_steps)
    while script_running:
        if script_paused or stuck:  # Check if the script is paused or character is stuck
            time.sleep(1)  # Wait until unpause or unstuck
            continue

        # Check if the time limit has been reached
        if time.time() - start_time > run_duration:
            break

        with stuck_lock:  # Acquire lock before checking the stuck flag
            if stuck:
                continue  # Skip the rest of the loop if stuck

        while counter_1 < (current_hunting_pattern.limit_1 * cyclone_adjustment):

            if not script_running or script_paused:
                break
            duration = (0.2 + random.uniform(-0.04, 0.04)) / cyclone_adjustment  # Randomize duration
            pyautogui.moveTo(next_steps[0], duration=duration)

            if stuck:
                handle_stuck(counter_1, next_steps[0][0], next_steps[0][1])

            keyboard.press("ctrl")
            pyautogui.leftClick()
            pyautogui.rightClick()
            counter_1 += 1
        time.sleep(0.35)  # Allow time for new pattern
        while counter_2 < (current_hunting_pattern.limit_2 * cyclone_adjustment):
            if not script_running or script_paused:
                break
            duration = (0.2 + random.uniform(-0.04, 0.04)) / cyclone_adjustment  # Randomize duration
            pyautogui.moveTo(next_steps[1], duration=duration)

            if stuck:
                handle_stuck(counter_2, next_steps[1][0], next_steps[1][1], direction=2)

            keyboard.press("ctrl")
            pyautogui.leftClick()
            pyautogui.rightClick()
            counter_2 += 1
        time.sleep(0.35)  # Allow time for new pattern
        while counter_3 < (current_hunting_pattern.limit_3 * cyclone_adjustment):
            if not script_running or script_paused:
                break
            duration = (0.2 + random.uniform(-0.04, 0.04)) / cyclone_adjustment  # Randomize duration
            pyautogui.moveTo(next_steps[2], duration=duration)

            if stuck:
                handle_stuck(counter_3, next_steps[2][0], next_steps[2][1], direction=3)

            keyboard.press("ctrl")
            pyautogui.leftClick()
            pyautogui.rightClick()
            counter_3 += 1
        time.sleep(0.35)  # Allow time for new pattern
        while counter_4 < (current_hunting_pattern.limit_4 * cyclone_adjustment):
            if not script_running or script_paused:
                break
            duration = (0.2 + random.uniform(-0.04, 0.04)) / cyclone_adjustment  # Randomize duration
            pyautogui.moveTo(next_steps[3], duration=duration)

            if stuck and False:
                handle_stuck(counter_4, next_steps[3][0], next_steps[3][1], direction=4)

            keyboard.press("ctrl")
            pyautogui.leftClick()
            pyautogui.rightClick()
            counter_4 += 1

            # Check if all loops are complete and not paused - Making sure all loops execute fully
        if (not script_paused and counter_1 >= current_hunting_pattern.limit_1
                and counter_2 >= current_hunting_pattern.limit_2
                and counter_3 >= current_hunting_pattern.limit_3
                and counter_4 >= current_hunting_pattern.limit_4):
            # Reset counters for next loop
            counter_1, counter_2, counter_3, counter_4 = 0, 0, 0, 0

        # Small delay to allow hotkey detection
        time.sleep(0.7)


# Function to check if character is stuck
def check_if_stuck():
    global prev_coor, stuck, stuck_counter
    print('Stuck Thread Starting...')
    time.sleep(2)  # Sleep at the start to give time for initial image capture
    while script_running:
        print("Parsing stuck thread with Stuck counter = ", stuck_counter)
        if script_paused:
            time.sleep(1)
            continue

        time.sleep(1.17)  # Time Between Checks
        with stuck_lock:  # Acquire lock before checking
            # print("Starting stuck capture...")
            current_coor = get_cq_map_coordinates()
            # print("Parsed stuck coordinates")
            if prev_coor is not None and current_coor is not None and prev_coor == current_coor and current_coor != '':
                stuck = True
                stuck_counter += 1
                print("Stuck at coordinates: ", current_coor, prev_coor)
            else:
                stuck = False
                stuck_counter = 0
            prev_coor = current_coor


def handle_stuck(counter, x_coords, y_coords, direction=1):
    global stuck, stuck_counter, counter_1, counter_2, counter_3, counter_4, script_paused, pattern_next_steps
    duration = (0.2 + random.uniform(-0.04, 0.04)) / cyclone_adjustment  # Randomize duration
    next_steps = pattern_next_steps

    if stuck and stuck_counter == 1:
        if direction == 1:
            pyautogui.moveTo(x_coords, y_coords - 96, duration=duration)
        elif direction == 2:
            pyautogui.moveTo(x_coords + 96, y_coords, duration=duration)
        elif direction == 3:
            pyautogui.moveTo(x_coords, y_coords - 96, duration=duration)
        elif direction == 4:
            pyautogui.moveTo(x_coords - 96, y_coords, duration=duration)
        counter -= 2
    elif stuck_counter == 3:
        if direction == 1:
            pyautogui.moveTo(x_coords, y_coords + 96, duration=duration)
        elif direction == 2:
            pyautogui.moveTo(x_coords - 200, y_coords, duration=duration)
        elif direction == 3:
            pyautogui.moveTo(next_steps[3], duration=duration)
        elif direction == 4:
            pyautogui.moveTo(x_coords + 96, y_coords, duration=duration)
        counter -= 1
    elif stuck_counter == 5:
        if direction == 1:
            pyautogui.moveTo(next_steps[1], duration=duration)
        elif direction == 2:
            pyautogui.moveTo(next_steps[2], duration=duration)
        elif direction == 3:
            pyautogui.moveTo(next_steps[3], duration=duration)
        elif direction == 4:
            pyautogui.moveTo(next_steps[0], duration=duration)
        counter -= 1
    elif stuck_counter > 6:
        print('Stuck for more than 5 seconds')
        script_paused = True

    # Updating counters based on the loop
    if direction == 1:
        counter_1 = counter
    elif direction == 2:
        counter_2 = counter
    elif direction == 3:
        counter_3 = counter
    elif direction == 4:
        counter_4 = counter


# Function to check HP threshold and get_out()
def check_hp_bar():
    global hp_threshold
    print('Hp Bar Thread Starting..')
    try:
        hp_bar = get_hpbar_coor()
        # print('HP Bar Coordinates:', hp_bar)
        hp_img = capture_screen_area(hp_bar)
        # Extract text from the image
        extracted_text = extract_text_from_image_hp(hp_img)
        # Attempt to extract and convert the HP value
        hp_value = int(extracted_text.split(" ")[1].split("/")[0])
        print("Current HP:", hp_value)
        if hp_value < hp_threshold:
            execute_get_out()
        return None
    except Exception as e:
        # Handle any exceptions that occur during the process
        print(f"An error occurred: {e}")
        # Optionally return None or a default value if there's an error
        return None


# Function to pause the script
def pause_script():
    global script_paused
    script_paused = True


# Function to resume the script
def resume_script():
    global script_paused, loot_counter
    loot_counter = 0
    script_paused = False


# Function to stop the script
def stop_script():
    global script_running, script_paused
    script_running = False
    keyboard.release("ctrl")  # Release Ctrl key when stopping


def loot_processing_task():
    global script_running, script_paused
    print('Loot Thread Starting..')
    while script_running:
        if script_paused:
            time.sleep(1)
            continue
        try:
            # Use FindChatFunction Module
            SystemChat_Loot = get_system_chat_coordinates()
            # Check if the coordinates are valid
            if not is_coordinates_valid(SystemChat_Loot):
                print(f"Loot Chat not Found or empty: {SystemChat_Loot}. Skipping to next iteration.")
                time.sleep(1.5)  # Wait a bit before next attempt, adjust time as necessary
                continue  # Skip the rest of this loop iteration

            img_loot = capture_screen_area(SystemChat_Loot)
            # print("Captured Image for Loot chat...")
            extracted_loot_text: str = extract_text_from_image(img_loot)
            # print("Parsed text..")
            check_loot(extracted_loot_text)
        except Exception as e:
            print(f"Error processing image or extracting text: {e}")
            # Optionally, you can log more details about the error or take additional recovery actions here.

        # Wait before next attempt, adjust time as necessary
        time.sleep(1.5)


def check_loot(extracted_loot_text):
    global script_paused, search_words, loot_counter
    # Check if any word in search_words is in extracted_text
    # print(extracted_loot_text)
    any_word_found = any(word in extracted_loot_text for word in search_words)

    if any_word_found:
        script_paused = True  # Pause the script because a specified Loot  was found
        if loot_counter < 1:
            winsound.Beep(440, 1000)  # Play a beep sound for notification
            loot_counter += 1

        print("Loot Found")


# Function to stop the engine and heal/tp home
def execute_get_out():
    global script_running

    # Release potentially held-down keys
    keyboard.release('ctrl')  # Add other keys if needed

    for _ in range(3):  # Heal
        keyboard.press_and_release('f1')
        time.sleep(1)
    for _ in range(2):  # Get out
        keyboard.press_and_release('f4')
        time.sleep(0.1)
    stop_script()


###################
# Starting Script #
###################
# Find Target client - Resize & Re_Center
print("Finding Game Client and re-sizing..")
find_target_client(char_name)


# Validating chat location for Socketing Success Task
print("Validating Chat UI integrity on screen..")
SystemChat = get_system_chat_coordinates()
validate_chat()

# Setting chat to "Loot" for loot processing task
print("Setting Chat Loot for loot processing..")
find_and_click_chat_button('Loot')

# Calculating Pattern steps & limits.
pattern_next_steps = find_pattern_steps(current_hunting_pattern.shape, current_hunting_pattern.start_point,
                                        current_hunting_pattern.start_direction, current_hunting_pattern.step_size)
# To be possibly later Developed pattern_limits = find_pattern_limits()

# Setting up hotkeys
keyboard.add_hotkey('ctrl+x', pause_script)  # Pause hotkey
keyboard.add_hotkey('ctrl+z', resume_script)  # Resume hotkey
keyboard.add_hotkey('ctrl+s', stop_script)  # Stop hotkey

# Start the threads
stuck_check_thread = threading.Thread(target=check_if_stuck)
hp_check_thread = threading.Thread(target=check_hp_bar)
loot_processing_thread = threading.Thread(target=loot_processing_task)
hp_check_thread.start()
stuck_check_thread.start()
loot_processing_thread.start()

# Start the script with a delay
print("Starting The Hunter..")
time.sleep(2)
script_thread = threading.Thread(target=hunting_engine)
script_thread.start()

# The script will run until stopped by the user
script_thread.join()
hp_check_thread.join()
stuck_check_thread.join()
loot_processing_thread.join()
