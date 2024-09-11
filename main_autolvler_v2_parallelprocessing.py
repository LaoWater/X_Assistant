import threading
import keyboard
import pyautogui
import time
import os
import numpy as np
from PIL import Image
from automation_engine import (capture_screen_area, get_hpbar_coor, extract_hp_value,
                               get_active_window_region_from_target_client, find_target_client)
from image_processing_engine import extract_text_from_image_hp
# from file_processing import screenshot_saving_to_file
import cv2

script_running = True
hp_thread_running = False
char_name = 'Old-Shepherd'

starting_color_mob_hp = (184, 3, 3)

# HP Thresholds
hp_potion_threshold = 500

# Original bypass_region in screen coordinates
# Originally developed on 1920x1080 PC, 1650x920 Game
self_hp_bar_y, self_hp_bar_x, self_hp_bar_width, self_hp_bar_height = 444, 934, 55, 9
bypass_region = (self_hp_bar_y, self_hp_bar_x, self_hp_bar_width, self_hp_bar_height)
window_region = (0, 0, 0, 0)

# Define the path for the 'TestingImages' directory in the current working directory
current_dir = os.path.dirname(__file__)  # Gets the directory of the current script
testing_images_dir = os.path.join(current_dir, 'TestingImages')

# Define the full path to save the image
image_save_path = os.path.join(testing_images_dir, 'SpiralParsedMatrixImage.png')


class StopScriptException(Exception):
    pass


def is_within_bypass_region(x, y, bp_region):
    by_top, by_left, by_width, by_height = bp_region
    # Convert to integers if they are not already, to prevent type errors
    by_top = int(by_top)
    by_left = int(by_left)
    by_width = int(by_width)
    by_height = int(by_height)
    x = int(x)
    y = int(y)
    return (by_left <= x < by_left + by_width) and (by_top <= y < by_top + by_height)


def adjust_coords_mother_system(x, y, adjustment_type):
    """Adjust coordinates between screen and screenshot coordinate systems."""
    global window_region  # Assuming window_region is defined globally
    window_left, window_top, _, _ = window_region

    if adjustment_type == "ToScreen":
        # Adjust from screenshot to screen coordinates
        adjusted_x = x + window_left
        adjusted_y = y + window_top
    elif adjustment_type == "ToScreenshot":
        # Adjust from screen to screenshot coordinates
        adjusted_x = x - window_left
        adjusted_y = y - window_top
    else:
        raise ValueError("Invalid adjustment_type. Use 'ToScreen' or 'ToScreenshot'.")

    return adjusted_x, adjusted_y


def find_pixel_by_color_in_active_window(color, tolerance=10):
    # Define the self HP bar control as a global bypass region
    global window_region, self_hp_bar_y, self_hp_bar_x, self_hp_bar_width, self_hp_bar_height

    # Adjust the bypass region to screenshot coordinate system
    adjusted_bypass_region_top_left = adjust_coords_mother_system(self_hp_bar_x, self_hp_bar_y, "ToScreenshot")

    adjusted_bypass_region = (adjusted_bypass_region_top_left[1], adjusted_bypass_region_top_left[0],
                              self_hp_bar_width, self_hp_bar_height)
    screenshot = pyautogui.screenshot(region=window_region)
    try:
        screenshot.save(image_save_path)
    except Exception as e:
        print(f"Error saving image: {e}")
        print(f"Image size: {screenshot.size}, Mode: {screenshot.mode}")
    # Convert the PIL image to a NumPy array for processing
    image_matrix = np.array(screenshot)

    # Use spiral search to find the pixel matching the target color
    found_pixel = spiral_search(image_matrix, color, tolerance, adjusted_bypass_region)
    if found_pixel:
        # Adjust found pixel coordinates back to screen coordinate system
        screen_x, screen_y = adjust_coords_mother_system(found_pixel[0], found_pixel[1], "ToScreen")
        # print(f"(Screenshot-System) Color found at screenshot-system coordinates: ({found_pixel})")
        # print(f"(Adjusted back to screen) Color found at screen coordinates: ({screen_x}, {screen_y})")
        return screen_x, screen_y

    # print("Color not found in 1st processing function.")
    return None


def spiral_search(image_matrix, target_color, tolerance, adjusted_bypass_region, step=4):
    spiral_start_time = time.time()
    height, width, _ = image_matrix.shape
    center_x, center_y = width // 2, (height // 2) - 40  # Character off-set
    direction = [(0, step), (step, 0), (0, -step), (-step, 0)]  # Directions: right, down, left, up
    x, y = center_x, center_y  # Start from the center
    step_size = 1
    direction_index = 0  # Start direction: right
    # You might adjust this range depending on how visible you want the marker to be
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if 0 <= center_x + dx < image_matrix.shape[1] and 0 <= center_y + dy < image_matrix.shape[0]:
                image_matrix[center_y + dy, center_x + dx] = [0, 0, 0]  # Marking in black

    image_matrix_parsed = image_matrix
    while 0 <= x < width and 0 <= y < height:
        for _ in range(2):  # Same step size for two directions then increase
            steps = step_size
            while steps > 0:
                if 0 <= x < width and 0 <= y < height:
                    # Check if within bypass region
                    if not is_within_bypass_region(x, y, adjusted_bypass_region):
                        pixel_color = image_matrix[y, x]
                        if np.all(np.abs(pixel_color - target_color) <= tolerance):
                            parsed_spiral_search = Image.fromarray(image_matrix_parsed.astype('uint8'))
                            parsed_spiral_search.save(image_save_path)
                            # Measuring time
                            print(f"Spiral search comupting time inside function: {time.time() - spiral_start_time}")
                            return x, y  # Found the target color

                        image_matrix_parsed[y, x] = [0, 0, 0]  # Marking parsed pixels for testing

                x += (direction[direction_index][0] * 2)
                y += direction[direction_index][1]
                steps -= 1
            direction_index = (direction_index + 1) % 4  # Change direction
        step_size += 1  # Increase step size after completing a   cycle in all directions

    parsed_spiral_search = Image.fromarray(image_matrix_parsed.astype('uint8'))
    parsed_spiral_search.save(image_save_path)
    return None  # Target color not found


def get_starting_pixel_color_manual():
    print("Hover over the target pixel and press ENTER to select the starting pixel color.")
    keyboard.wait('enter')  # Wait for the user to press ENTER
    x, y = pyautogui.position()  # Get the current mouse position
    starting_color = pyautogui.screenshot().getpixel((x, y))  # Get the color at the mouse position

    return starting_color


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


def stop_script():
    """Set the script_running flag to False to stop the script."""
    global script_running
    script_running = False


def explore_and_bound_hp_bar(image, start_x, start_y):
    target_color = starting_color_mob_hp
    stack = [(start_x, start_y)]
    min_x, max_x = start_x, start_x
    min_y, max_y = start_y, start_y

    visited = {start_x, start_y}

    while stack:
        x, y = stack.pop()

        # Update bounds
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

        # Check and add neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < image.shape[1] and 0 <= ny < image.shape[0]:  # Stay within image bounds
                if (nx, ny) not in visited and all(image[ny, nx, :3] == target_color):  # Match color
                    stack.append((nx, ny))
                    visited.add((nx, ny))

    return min_x, min_y, max_x - min_x + 1, max_y - min_y + 1


def find_and_draw_first_hp_bar(image, start_pixel_x, start_pixel_y):
    # Convert target_color to RGB if your image is in RGB

    if start_pixel_x is None:
        print("No matching pixel found.")
        return None

    # Expand from the first pixel to find the bounds
    bounds = explore_and_bound_hp_bar(image, start_pixel_x, start_pixel_y)

    # Drawing bounding box for visual verification
    if bounds:
        cv2.rectangle(image, (bounds[0], bounds[1]), (bounds[0] + bounds[2], bounds[1] + bounds[3]), (0, 255, 0), 2)
        # Save or display the image to verify the result
        # cv2.imwrite('first_hp_bar_detected.png', image)
        return bounds
    else:
        return None


def adjust_for_bgra(image):
    # If the image is BGRA, convert to RGB
    if image.shape[2] == 4:
        # Convert BGRA to BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        # Then convert BGR to RGB if your processing assumes RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def check_stop():
    global script_running

    if not script_running:
        print("Stopping Script from check_stop function call in main engine")
        raise StopScriptException()  # Raise custom exception to stop the script

    return False  # Continue script_running


def find_first_hp_bar():
    global starting_color_mob_hp, window_region
    found_pos = find_pixel_by_color_in_active_window(starting_color_mob_hp)
    print("Found Target color at pixel-pos:", found_pos)
    if found_pos is None:
        time.sleep(1)
        return None
    screenshot_cq = capture_screen_area(window_region)
    # Convert MSS screenshot (chosen for efficiency) to BGRA (PIL format)
    screenshot_bgra = adjust_for_bgra(screenshot_cq)
    found_hp_bar_adjusted = adjust_coords_mother_system(found_pos[0], found_pos[1], 'ToScreenshot')
    found_hp_bar_ss_bounds = find_and_draw_first_hp_bar(screenshot_bgra, found_hp_bar_adjusted[0],
                                                        found_hp_bar_adjusted[1])

    # Ensure find_and_draw_first_hp_bar returns a list or convert its result to a list if it's a tuple
    if isinstance(found_hp_bar_ss_bounds, tuple):
        found_hp_bar_ss_bounds = list(found_hp_bar_ss_bounds)

    found_hp_bar_system_adjusted_tl = adjust_coords_mother_system(found_hp_bar_ss_bounds[0],
                                                                  found_hp_bar_ss_bounds[1], 'ToScreen')
    found_hp_bar_system_adjusted_bounds = (found_hp_bar_system_adjusted_tl,
                                           found_hp_bar_ss_bounds[2], found_hp_bar_ss_bounds[3])
    print("(System Adjusted) First Found HP_Bar Bounds:", found_hp_bar_system_adjusted_bounds)
    # Calculating Mob % HP with default 50 width - to get the exact X-Center
    hp_bar_center_x = found_hp_bar_system_adjusted_tl[0] + 25
    hp_bar_center_y = found_hp_bar_system_adjusted_tl[1] + 15
    return hp_bar_center_x, hp_bar_center_y


def main():
    global script_running, starting_color_mob_hp, window_region, hp_thread_running

    # Find Target client - Resize & Re_Center
    find_target_client(char_name)
    window_region = get_active_window_region_from_target_client(char_name)
    print(window_region)
    time.sleep(2)

    try:
        while script_running:
            hp_thread_running = True
            start_time = time.time()
            found_pos = find_first_hp_bar()

            if found_pos:
                # Calculate the elapsed time
                elapsed_time = time.time() - start_time
                print(f"Clicking at {found_pos}... Time elapsed: {elapsed_time:.2f} seconds")
                pyautogui.click(found_pos)

            else:
                print(f"Color not found on screen. Re-trying..")

            time.sleep(2)
            if check_stop():
                raise StopScriptException()
        print("Script stopped.")

    except StopScriptException:
        print("Script stopped.")


if __name__ == "__main__":
    keyboard.add_hotkey('space', stop_script)  # Stop hotkey
    hp_check_thread = threading.Thread(target=check_hp_bar)
    hp_check_thread.start()

    main()

    hp_check_thread.join()
