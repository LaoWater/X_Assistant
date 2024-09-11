import math
import pyautogui
import time
import numpy as np
import mss
import pygetwindow as gw
from PIL import Image
import pytesseract
import os
from image_processing_engine import read_text_from_image
from file_processing import screenshot_saving_to_file
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global flag to control the script's execution
stop_script = False

# Global Flag - Set to True first time running on new environment
new_environment = False  # Set to False if not setting up in a new environment with different Resolution than 1920x1080

# Get the size of the screen
screenWidth, screenHeight = pyautogui.size()

# Replace these with your PC/laptop's Resolution (Right Click->Display Settings)
width_pixels = 1920
height_pixels = 1080
diagonal_inches = 15.6  # Laptop Value

# Game Resolutions
# Developed on 1650x900 with game always centered.
from_reso = (1650, 920)
to_resolution = (1800, 980)

# Customizable Loot stopping words
search_words = ['Ring', 'DragonBall', 'Necklace', 'Super', 'Boots', 'Bow', 'SuperDragonBall', 'Bag']

# Monitor areas for stuck handling (character stopped movement based on game coordinates)
# ****  Game Coordinates *****
# * PPI dependent - initially measured on 1800x980
game_coordinates_y = 119
game_coordinates_x = 246
game_coordinates_width = 65  # Default i think
game_coordinates__height = 17
coordinates_capture = {'top': game_coordinates_y, 'left': game_coordinates_x,
                       'width': game_coordinates_width, 'height': game_coordinates__height}

# Images Path
# Define the base path for images
image_base_path = 'Images'

coat_path = os.path.join(image_base_path, 'TheSocketeer_images', 'coat.png')
try:
    img = Image.open(coat_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{coat_path}' not found in the specified directory.")

# Using os.path.join to construct file paths
warehouse_path = os.path.join(image_base_path, 'warehouse_mapping.PNG')
try:
    img = Image.open(warehouse_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{warehouse_path}' not found in the specified directory.")

hpbar_path = os.path.join(image_base_path, 'hp_image.PNG')
try:
    img = Image.open(hpbar_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{hpbar_path}' not found in the specified directory.")

system_button_path = os.path.join(image_base_path, 'system_button.PNG')
try:
    img = Image.open(system_button_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{system_button_path}' not found in the specified directory.")

loot_button_path = os.path.join(image_base_path, 'loot_button.PNG')
try:
    img = Image.open(loot_button_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{loot_button_path}' not found in the specified directory.")

inventory_path = os.path.join(image_base_path, 'TheSocketeer_images', 'inventory.png')
try:
    img = Image.open(inventory_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{inventory_path}' not found in the specified directory.")

system_chat_im_path1 = os.path.join(image_base_path, 'System_Chat_Top.JPG')
try:
    img = Image.open(system_chat_im_path1)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{system_chat_im_path1}' not found in the specified directory.")

system_chat_im_path2 = os.path.join(image_base_path, 'System_Chat_Bottom.JPG')
try:
    img = Image.open(system_chat_im_path2)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{system_chat_im_path2}' not found in the specified directory.")

system_chat_im_path3 = os.path.join(image_base_path, 'System_Chat_Right.JPG')
try:
    img = Image.open(system_chat_im_path3)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{system_chat_im_path3}' not found in the specified directory.")

# Global flags and counters
script_running = True
script_paused = False
stuck = False
hp_bar_changed = False
counter_1, counter_2, counter_3, counter_4 = 0, 0, 0, 0
stuck_counter = 0
prev_coor = ''
prev_img_hp = None
loot_counter = 0

# Errors logging
errors = []


def get_cq_map_coordinates():
    global coordinates_capture
    image = capture_screen_area(coordinates_capture)
    text = read_text_from_image(image)
    numbers = re.findall(r'\d+', text)

    # Validate that we have exactly two numbers and each number has a maximum length of 3 digits
    # v[2.0] - Check for numbers to have length of 3 - meaning the coordinates were correctly read from image
    # Necessary change as the OCR was sometimes miss-reading.
    if len(numbers) == 2 and all(len(num) == 3 for num in numbers):
        current_coor = tuple(map(int, numbers))
        return current_coor
    else:
        # Return None if the coordinates are not in the expected format
        return None


def adjust_cq_map_coordinates(current_reso):
    # Adjust game coordinates location based on resolution
    global coordinates_capture, from_reso
    if from_reso != current_reso:
        adj_coords = adjust_coordinates_relative(game_coordinates_y, game_coordinates_x, from_reso, current_reso)
        coordinates_capture['top'] = adj_coords[1]
        coordinates_capture['left'] = adj_coords[0]
    image = capture_screen_area(coordinates_capture)
    screenshot_saving_to_file(image, 'CoordinatesTest.png')
    # current_coor = read_text_from_image(image)

    return None


# Function to calculate PPI (Pixels Per Inch)
def calculate_ppi(width_p, height_p, diagonal_inch):
    return ((width_p ** 2 + height_p ** 2) ** 0.5) / diagonal_inch


# Global variables are declared here to store base and target PPI values, calculated using the above function.

# Base system PPI (e.g., your development PC)
base_ppi = calculate_ppi(1920, 1080, 27)  # Example: 27-inch monitor

# Target system PPI (e.g., a different PC or laptop where the script will run)
target_ppi = calculate_ppi(1920, 1080, 27)  # Example: 27-inch laptop, adjust as needed

# Calculate the adjustment factor based on the PPI values
adjustment_factor = target_ppi / base_ppi


# Function to adjust values (e.g., image sizes, coordinates) based on the adjustment factor
def adjust_value(x):
    return int(x * adjustment_factor)


def find_target_client(char_name):
    # Find the currently active window
    target_window_title = char_name
    # Wait for the window with the target title to become the active one
    while True:
        active_window = gw.getActiveWindow()
        if char_name in active_window.title:
            # Adjust Game Resolution to Default - If changed then Adjustment Factor needs to be calculated & applied.
            resize_and_center_window(target_window_title, 1650, 920)
            break  # Exit the loop since the desired window is found and active
        else:
            print(f"Please open {char_name} Game Client.")
            # If the desired window is not active, wait a bit before checking again
            time.sleep(3)  # Adjust the sleep time as necessary


def get_active_window_region_from_target_client(target_client):
    active_window = gw.getActiveWindow()
    # Check if there is an active window and if its title matches the specified target client
    if active_window and target_client in active_window.title:
        # If the active window's title matches the target client, return its region
        return active_window.left, active_window.top, active_window.width, active_window.height
    else:
        # If no active window matches the specified target client, return None
        return None


def capture_screen_area(monitor):
    with mss.mss() as sct:
        try:
            screenshot = sct.grab(monitor)
            return np.array(screenshot)
        except Exception as e:  # Catching any exception and printing it
            print('An error occurred during capture:', e)
            exit()


def resize_and_center_window(window_title, width=1650, height=920):
    try:
        time.sleep(1)
        # Get the window
        window = gw.getWindowsWithTitle(window_title)[0]

        # Resize the window
        window.resizeTo(width, height)

        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()

        # Calculate the x and y coordinates to center the window
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        # Ensure x and y are within screen bounds
        x = max(0, min(x, screen_width))
        y = max(0, min(y, screen_height))

        # Move the window
        window.moveTo(x, y)

        # Map cq_map_chat coordinates to new system if necessary
        current_resolution = width, height
        adjust_cq_map_coordinates(current_resolution)
    except Exception as e:
        print(f"Error: {e}")


def find_image(image_path: str, confidence: float = 0.80):
    global errors
    try:
        # Locate all instances of the image on the screen
        boxes = pyautogui.locateAllOnScreen(image_path, confidence=confidence)

        # Convert Box objects to tuples
        locations = [(box.left, box.top, box.width, box.height) for box in boxes]

        if locations:
            centerScreenX, centerScreenY = screenWidth / 2, screenHeight / 2

            # Find the image closest to the screen center
            closest_location = min(locations, key=lambda loc: math.hypot(centerScreenX - pyautogui.center(loc)[0],
                                                                         centerScreenY - pyautogui.center(loc)[1]))

            # Get the center coordinates of the closest image
            center_x, center_y = pyautogui.center(closest_location)

            # Return the coordinates
            return center_x, center_y

        else:
            print("No locations found")

    except pyautogui.ImageNotFoundException:
        # Handle the exception for when the image is not found
        print("Chat not found on screen.")

    except Exception as e:
        errors.append(f"Image: {image_path}, {e}")

    # Return None if no image is found or an exception occurs
    return None


def find_image_top_left_coor(image_path: str, confidence: float = 0.93):
    try:
        # Locate all instances of the image on the screen
        boxes = pyautogui.locateAllOnScreen(image_path, confidence=confidence)

        # Convert Box objects to tuples
        locations = [(box.left, box.top, box.width, box.height) for box in boxes]

        if locations:
            centerScreenX, centerScreenY = screenWidth / 2, screenHeight / 2

            # Find the image closest to the screen center
            closest_location = min(locations, key=lambda loc: math.hypot(centerScreenX - pyautogui.center(loc)[0],
                                                                         centerScreenY - pyautogui.center(loc)[1]))

            # closest_location already contains the top-left coordinates as (left, top, width, height)
            top_left_x, top_left_y = closest_location[0], closest_location[1]

            # Return the top-left coordinates
            return top_left_x, top_left_y

        else:
            print("No locations found")

    except pyautogui.ImageNotFoundException:
        # Handle the exception for when the image is not found
        print("Image not found on screen.")

    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")

    # Return None if no image is found or an exception occurs
    return None


def get_hpbar_coor():
    hpbar_coordinates = find_image_top_left_coor(hpbar_path)
    if hpbar_coordinates:
        # print(f"Image found at coordinates: {hpbar_coordinates}")
        # Calculate the coordinates for the first inventory item
        hpbar_coor_x = hpbar_coordinates[0]
        hpbar_coor_y = hpbar_coordinates[1]
        hpbar_width = 100
        hpbar_height = 17
        hp_bar = {'top': hpbar_coor_y, 'left': hpbar_coor_x, 'width': hpbar_width, 'height': hpbar_height}
        return hp_bar
    else:
        # Return None or some default coordinates if the image is not found
        return None, None


def extract_hp_value(extracted_text):
    # Find the position of 'HP: '
    hp_pos = extracted_text.find('HP: ')
    if hp_pos == -1:
        print("The string 'HP: ' was not found in the extracted text.")
        return None

    # Find the position of '/' starting from the position of 'HP: '
    slash_pos = extracted_text.find('/', hp_pos)
    if slash_pos == -1:
        print("The character '/' was not found in the extracted text.")
        return None

    # Extract the HP value string by slicing from 'HP: ' to '/'
    hp_value_str = extracted_text[hp_pos + 4:slash_pos]
    try:
        hp_value = int(hp_value_str)
        return hp_value
    except ValueError:
        print("Failed to convert extracted HP value to an integer.")
        return None


def get_system_chat_coordinates():
    # Dynamic Coordinates - Mother PPI is 1650x920, 27-inch
    # system_chat_w = 422  # Default pixels values I think?
    system_chat_y_scaling = 10  # Therefore, leave Inch value from PPI calculations below unchanged
    system_chat_h_scaling = 25

    # Get the center coordinates of the images
    system_chat_coordinates1 = find_image(system_chat_im_path1)
    system_chat_coordinates2 = find_image(system_chat_im_path2)
    system_chat_coordinates3 = find_image(system_chat_im_path3)

    if system_chat_coordinates1 and system_chat_coordinates2 and system_chat_coordinates3:
        system_chat_x = system_chat_coordinates1[0]
        system_chat_x = system_chat_x - 15
        system_chat_y = system_chat_coordinates1[1] + system_chat_y_scaling
        # Calculate system_chat_h ensuring it does not exceed the screen's bottom edge
        system_chat_w_temp = int(system_chat_coordinates3[0] - system_chat_x)
        system_chat_w = min(system_chat_w_temp, screenWidth - system_chat_x)
        system_chat_h_temp = int(system_chat_coordinates2[1] - system_chat_coordinates1[1] - system_chat_h_scaling)
        system_chat_h = min(system_chat_h_temp, screenHeight - system_chat_y)

        sys_chat = {'top': system_chat_y, 'left': system_chat_x, 'width': system_chat_w, 'height': system_chat_h}
        return sys_chat

    else:
        print("Chat not found. Re-trying..")
        time.sleep(5)

    return None


def is_coordinates_valid(coords):
    # Check if coords is None
    if coords is None:
        return False
    # Assuming screen resolution or valid coordinate ranges are known, checks if provided coordinates are valid
    screen_width, screen_height = 1920, 1080  # Example values, adjust as necessary
    x = int(coords['left'])
    y = int(coords['top'])
    w = int(coords['width'])
    h = int(coords['height'])

    return (0 <= x <= screen_width and 0 <= y <= screen_height and w > 0 and h > 0
            and x + w <= screen_width and y + h <= screen_height)


def warehouse_coor(max_attempts=10):
    i = 0
    while i < max_attempts:
        wh_coordinates = find_image(warehouse_path)
        if wh_coordinates:
            print("Found warehouse image at", wh_coordinates)
            return wh_coordinates
        else:
            i += 1
            print(f"Mapping Warehouse Attempt {i}..")
            time.sleep(1)
    print("Failed to find warehouse coordinates after", max_attempts, "attempts.")
    return None


def inventory_coor():
    inventory_coordinates = find_image(inventory_path)
    if inventory_coordinates:
        # print(f"Inventory coordinates found at: {inventory_coordinates}")
        first_inv_item_x = inventory_coordinates[0]
        first_inv_item_y = inventory_coordinates[1]
        return first_inv_item_x, first_inv_item_y
    else:
        # Return None or some default coordinates if the image is not found
        return None, None


def socketed_item_coor(item):
    item_path = os.path.join(image_base_path, 'TheSocketeer_images', f'{item}.png')
    item_coordinates = find_image(item_path)
    if item_coordinates:
        # print(f"Desired socketed item found at coordinates: {item_coordinates}")
        # Calculate the coordinates for the first inventory item
        first_inv_item_x = item_coordinates[0]
        first_inv_item_y = item_coordinates[1]
        return first_inv_item_x, first_inv_item_y
    else:
        # Return None or some default coordinates if the image is not found
        return None, None


# Function to adjust (x,y) coordinates on same PC resolution but different game resolutions & Screen Center
# Note that only the coordinates for elements on the edges should be targeted.
def adjust_coordinates_relative(relative_top, relative_left, from_res, to_res):
    # Calculate the relative positions
    negative_value_control = 1
    if from_res < to_res:
        negative_value_control = -1
    relative_left = relative_left + negative_value_control * ((from_res[0] - to_res[0]) / 2)
    relative_top = relative_top + negative_value_control * ((from_res[1] - to_res[1]) / 2)

    # Apply the relative positions to the target resolution
    adjusted_left = round(relative_left)
    adjusted_top = round(relative_top)

    return adjusted_top, adjusted_left


def find_and_click_chat_button(chat_type):
    try:
        if chat_type == 'system':
            image_path = system_button_path
        else:
            image_path = loot_button_path
        button_coordinates = find_image(image_path)
        if button_coordinates is not None:
            pyautogui.moveTo(button_coordinates, duration=0.2)
            pyautogui.click()
            time.sleep(0.2)
        else:
            print(f"Error: The button for {chat_type} chat was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def validate_chat():
    SystemChat = get_system_chat_coordinates()
    retry_limit = 5  # Maximum number of retries to find chat coordinates
    retry_count = 0  # Current retry attempt count
    # Getting system chat coordinates for socketing_task
    while SystemChat is None:
        SystemChat = get_system_chat_coordinates()
        if retry_count < retry_limit:
            print(f"Could not map chat coordinates. Attempt {retry_count + 1} of {retry_limit}...")
            retry_count += 1
            time.sleep(1)  # Wait a bit before retrying
            continue
        else:
            # After reaching retry limit, wait longer or handle the failure differently
            print("Reached retry limit. Will continue to check for chat coordinates...")
            time.sleep(5)  # Wait longer before checking again
            retry_count = 0  # Reset retry count if you wish to attempt retries again after some time
            continue
    return SystemChat
