# ----------------------------------------------------------------------------------------------
# The Hunter
#
# This tool is an image-processing socketing-bot for X online.
#
# Author :  Neo
# ----------------------------------------------------------------------------------------------

import time
import pyautogui
from pynput.mouse import Button, Controller as MouseController
import keyboard
import threading
import random
import pytesseract
import winsound
from automation_engine import (capture_screen_area, find_and_click_chat_button, warehouse_coor,
                               inventory_coor, find_target_client, socketed_item_coor,
                               get_cq_map_coordinates,
                               validate_chat)
from file_processing import save_excel_with_formatting, read_excel_counters
from image_processing_engine import extract_text_from_image
from main_databases import get_coord, custom_map_coordinates

# Configure the path to Tesseract in your system
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to your Accountant Excel file
excel_file = r'Accountant.xlsx'  # Update with your path

# Global values for Image Processing - Stopping at first successful socket
char_name = 'Lao'  # Current Character: Lao, BeWater
socketed_item = 'necklace'
characters = ['BeWater', 'Arsonist', 'Lao', 'TheHunt(er)', 'Old-Shepherd']  # All user Characters used for Socketing
search_words = [char_name, 'Amazing!', 'socket', 'first', 'upgraded']  # Replace with actual words

# Global variables for Coordinates
# For custom, set coord_Type to custom_X reference and map the new Coordinates if new Custom_1, or Default
coord_type = 'Default'
# custom_map_coordinates()

# NPCs Coordinates
# Originally developed on 1920x1080 PC, 1650x920 Game
Shopkeeper_X, Shopkeeper_Y = get_coord('Shop', coord_type)
Warehouse_X, Warehouse_Y = get_coord('Warehouse', coord_type)
Artisan_Wind_X, Artisan_Wind_Y = get_coord('Artisan_Wind', coord_type)
Upgrade_X, Upgrade_Y = get_coord('Upgrade', coord_type)

# In case someone blocking head - 305 default head value, 285 body
# Warehouse_Y += 20

# Set No. Of Socketing cycles. ( Recommended = 3 )
socketing_cycles = 3

# Setting Global Empty variables
B1_X = 0
B1_Y = 0
First_Meteor_Position_X = 0
First_Meteor_Position_Y = 0
First_WH_Meteor_Scroll_Y = 0
First_WH_Meteor_Scroll_X = 0
socketed_item_x = 0
socketed_item_y = 0
shopkeeper_buy_20_x = 0
shopkeeper_buy_20_y = 0
counter_meteors = 0
# Creating Current Items Lists to be used in Socketing_success
current_item_x = [[0] * 10 for _ in range(2)]
current_item_y = [[0] * 10 for _ in range(2)]

# Global flags for script control
script_running = True
chat_parsing_running = False
SocketSuccess = False
prev_coor = None

# Exploring alternate libraries for mouse & keyboard output
mouse = MouseController()


class StopScriptException(Exception):
    pass


def chat_parsing_task():
    global chat_parsing_running, script_running
    time.sleep(0.5)
    loop_start_time = time.time()
    while script_running:
        while script_running and chat_parsing_running:
            img = capture_screen_area(SystemChat)
            extracted_text = extract_text_from_image(img)
            check_for_socket(extracted_text)
            time.sleep(1)  # Adjust as necessary
            # Calculate time spent in chat parsing
            elapsed_time = time.time() - loop_start_time
            loop_start_time = time.time()  # Reset the start time for the next iteration
            print("Time between Chat parsings:", elapsed_time)
    # Sleep while socketing_task is not at upgrading step
    time.sleep(1)


def find_value_of_second_to_last_successful_task(matrix):
    print(f"Entering function with matrix:\n{matrix}")  # Print matrix at the start

    # Initialize tracking index for socket
    socket_index = -1

    # Initialize loop indices
    i, j = 0, 0

    # Iterate over the matrix to find the first socket
    while socket_index == -1 and i < len(matrix):
        row = matrix[i]

        while socket_index == -1 and j < len(row):
            item = row[j]
            print(f"Checking item at position ({i}, {j}): {item}")  # Print current item being checked

            # If a socket is found (item is 0 or None)
            if item == 0 or item is None:
                print(f"Socket found at position ({i}, {j}).")  # Print socket location
                # Update tracking index for the found socket
                socket_index = i * len(row) + j  # Convert 2D index to 1D index
            else:
                j += 1  # Move to the next column

        if socket_index == -1:  # If socket not found, move to the next row
            i += 1
            j = 0  # Reset column index for the next row

    if socket_index == -1:
        print("No socket found in the matrix.")
    else:
        print(f"Socket found at index {socket_index} in matrix. Iterating matrix to go back 2 positions")

    # Going back 2 items and returning
    control_index = 0
    if socket_index == 0:
        print("First item is a socket.")
        return matrix[0][0]

    # Iterate again to find the item 2 positions before the socket
    for i, row in enumerate(matrix):
        for j, item in enumerate(row):
            if control_index == (socket_index - 3):
                print(f"\nReached item before socket at position {control_index} and pixel position {matrix[i][j]}")
                return matrix[i][j]
            control_index += 1


def check_for_socket(extracted_text):
    global characters, char_name, SocketSuccess, script_running, current_item_x, current_item_y
    all_words_found = all(word in extracted_text for word in search_words)
    if all_words_found:
        script_running = False
        # Notifying User
        SocketSuccess = True
        pyautogui.keyUp('shift')
        time.sleep(0.7)
        winsound.Beep(440, 1000)  # 440 Hz for  1000 ms

        # Moving Socketed Item to Warehouse
        pyautogui.press('esc')
        pyautogui.moveTo(Warehouse_X, Warehouse_Y, duration=0.5)  # Warehouse
        pyautogui.click()
        # Print current_Item before calling the function
        print(f"Calling function with current_Item x {current_item_x} \n")
        print(f"Calling function with current_Item x {current_item_y} \n")
        x_successful_socket = find_value_of_second_to_last_successful_task(current_item_x)
        y_successful_socket = find_value_of_second_to_last_successful_task(current_item_y)
        print(f"\n\n x successful socket: {x_successful_socket} \n y successful socket: {y_successful_socket}")
        print("Successful Socket Coordinates", x_successful_socket, y_successful_socket)
        # Making sure Inventory is active window
        pyautogui.leftClick(B1_X, B1_Y, duration=0.5)
        time.sleep(0.2)
        pyautogui.keyDown('shift')
        pyautogui.moveTo(x_successful_socket, y_successful_socket, duration=0.5)
        # Bagging last 2 items in offset of socketing incrementation completing before reading Stop flag from chat p.
        for _ in range(2):
            pyautogui.leftClick()
            time.sleep(0.5)

        pyautogui.keyUp('shift')

        # Notifying User
        print("Successfully socketed! Stopping script...")


def check_if_moved():
    global script_running, prev_coor

    while script_running:
        current_coor = get_cq_map_coordinates()
        # print("Parsed stuck coordinates")
        if prev_coor is not None and current_coor is not None and prev_coor != current_coor and current_coor != '':
            print("Character moved. Stopping script..")
            print(f"Current Coordinates: {current_coor}")
            print(f"Previous Coordinates: {prev_coor}")
            script_running = False
        prev_coor = current_coor
        time.sleep(2.5)


def check_stop():
    global script_running, SocketSuccess, counter_meteors
    # Check coordinates to see if moved - greatly impacts performance
    # check_if_moved()
    if not script_running and not SocketSuccess:
        print("Stopping Script from check_stop function call in main engine")
        df = read_excel_counters(characters)
        # Apply Formatting
        save_excel_with_formatting(df, counter_meteors, char_name)
        time.sleep(1)
        raise StopScriptException()  # Raise custom exception to stop the script

    if not script_running and SocketSuccess:
        print("Stopping Script from check_socket function")
        df = read_excel_counters(characters)
        df.at['Successes', char_name] += 1
        save_excel_with_formatting(df, counter_meteors, char_name)
        time.sleep(1)
        raise StopScriptException()

    return False  # Continue running


def stop_script():
    global script_running
    script_running = False
    print("Stopping script manually... Good Luck next time!")


def socketing_task():
    global script_running, counter_meteors, current_item_x, current_item_y, chat_parsing_running, socketing_cycles, \
        B1_X, B1_Y

    socketing_cycle_no = 1
    try:
        while script_running and socketing_cycle_no <= socketing_cycles:
            if check_stop():
                break  # Check if script should stop naturally, not through Exception

            # Re-setting current item 2D lists - used for successful socket bagging
            current_item_x = [[0] * 10 for _ in range(2)]
            current_item_y = [[0] * 10 for _ in range(2)]

            # Open Shop & Buy 20 items
            if socketing_cycle_no > -1:
                pyautogui.moveTo(Shopkeeper_X, Shopkeeper_Y, duration=0.25)  # Shopkeeper
                pyautogui.click()

            pyautogui.moveTo(socketed_item_x, socketed_item_y)
            # Buy 20 items of desired item
            pyautogui.keyDown('shift')
            pyautogui.rightClick()
            pyautogui.keyUp('shift')
            time.sleep(0.10)  # Delay for "Buy 20" GUI to load
            pyautogui.click(shopkeeper_buy_20_x, shopkeeper_buy_20_y, duration=0.40)
            if check_stop():
                raise StopScriptException()
            pyautogui.press('esc')

            # Moving to Warehouse to take MS
            pyautogui.moveTo(Warehouse_X, Warehouse_Y, duration=0.3)
            if check_stop():
                raise StopScriptException()
            pyautogui.click()

            pyautogui.moveTo(First_WH_Meteor_Scroll_X, First_WH_Meteor_Scroll_Y,
                             duration=0.8)  # Take 1st WH Met Scroll (2x), wait for WH to Load
            pyautogui.click()
            time.sleep(0.7)  # Take 2nd WH Met Scroll
            pyautogui.click()
            pyautogui.press('esc')
            pyautogui.moveTo(First_Meteor_Position_X, First_Meteor_Position_Y, duration=0.4)  # 1st Met position
            for _ in range(2):  # Open MS, give slight delay for ping/server communication
                if check_stop():
                    raise StopScriptException()
                pyautogui.rightClick()
                time.sleep(1.25)

            cur_boots_y = B1_Y  # Save 1st Item position for finding the next line
            # Starting CHat_parsing_task for socketing search
            chat_parsing_running = True

            for i in range(2):  # Starting Socketing Attempts
                cur_boots_x = B1_X
                loop_start_time = time.time()
                for _ in range(10):  # Repeat the sequence 10 times
                    current_item_x[i][_] = cur_boots_x
                    current_item_y[i][_] = cur_boots_y
                    random_interval = random.uniform(0.06, 0.08)
                    if check_stop():
                        raise StopScriptException()

                    pyautogui.moveTo(Artisan_Wind_X, Artisan_Wind_Y, duration=0.4)  # Artisan Wind
                    pyautogui.click()

                    pyautogui.moveTo(cur_boots_x, cur_boots_y, duration=random_interval)  # B1
                    pyautogui.keyDown('shift')
                    pyautogui.click()

                    pyautogui.moveTo(First_Meteor_Position_X, First_Meteor_Position_Y,
                                     duration=random_interval)  # 1st Met position
                    pyautogui.click()

                    pyautogui.keyUp('shift')
                    if check_stop():
                        raise StopScriptException()
                    pyautogui.moveTo(Upgrade_X, Upgrade_Y, duration=random_interval)  # Upgrade
                    counter_meteors += 1
                    pyautogui.click()

                    cur_boots_x += 40

                    # Calculate and print elapsed time
                    elapsed_time = time.time() - loop_start_time
                    print("Time taken for Socket-Operation:", elapsed_time)

                    # Update loop start time for next iteration
                    loop_start_time = time.time()

                cur_boots_y += 40

            pyautogui.moveTo(Shopkeeper_X, Shopkeeper_Y, duration=0.7)  # Shopkeeper
            pyautogui.click()
            chat_parsing_running = False
            pyautogui.moveTo(B1_X, B1_Y, duration=0.2)  # First Inventory Item Position
            for _ in range(27):  # Sell upgraded Boots
                start_time = time.time()
                pyautogui.keyDown('shift')
                mouse.click(Button.left)
                pyautogui.keyUp('shift')
                if check_stop():
                    raise StopScriptException()
                print("Sell Item time between executions", time.time() - start_time)

            time.sleep(0.1)  # Time Between socketing cycles.
            if check_stop():
                raise StopScriptException()
            pyautogui.press('esc')
            print("Socketing cycle finished. Re-starting...")
            socketing_cycle_no += 1

    except StopScriptException:
        print("Socketing Task stopped.")

    print("Full Socketing cycles completed:", socketing_cycle_no - 1)
    script_running = False


def mapping_inventory_and_shop():
    global B1_X, B1_Y, First_Meteor_Position_X, First_Meteor_Position_Y, socketed_item_x, socketed_item_y, \
        shopkeeper_buy_20_x, shopkeeper_buy_20_y

    # Opening Shop & Mapping coordinates
    print("Mapping desired socketed item and inventory positions..")
    pyautogui.moveTo(Shopkeeper_X, Shopkeeper_Y, duration=0.30)
    pyautogui.click()
    b1_x_no_offset, b1_y_no_offset = inventory_coor()
    while b1_x_no_offset is None:
        print("Open Inventory for mapping..")
        time.sleep(1)
        b1_x_no_offset, b1_y_no_offset = inventory_coor()

    # Inventory Coordinates mapped from found 'Silver' image T-L value
    B1_X = b1_x_no_offset - 4
    B1_Y = b1_y_no_offset - 182
    First_Meteor_Position_X = B1_X
    First_Meteor_Position_Y = B1_Y + 80

    # print("Socketed Item X,Y)", socketed_item_x, socketed_item_y)
    # Find & Map Socketed Item
    socketed_item_x, socketed_item_y = socketed_item_coor(socketed_item)
    # Map "Buy 20x socketed item" coordinates
    shopkeeper_buy_20_x, shopkeeper_buy_20_y = socketed_item_x + 34, socketed_item_y + 47

    pyautogui.press('esc')


def mapping_warehouse():
    global First_WH_Meteor_Scroll_X, First_WH_Meteor_Scroll_Y
    print("Mapping Warehouse positions..")
    pyautogui.moveTo(Warehouse_X, Warehouse_Y, duration=0.25)
    pyautogui.click()
    time.sleep(0.1)  # Higher loading time for WH
    wh_x, wh_y = warehouse_coor()
    while First_WH_Meteor_Scroll_X is None:
        print("Open Warehouse for mapping..")
        time.sleep(1)
        wh_x, wh_y = warehouse_coor()
    First_WH_Meteor_Scroll_Y = wh_y + 33
    First_WH_Meteor_Scroll_X = wh_x - 108
    pyautogui.press('esc')


###################
# Starting Script #
###################
# Find Target client - Resize & Re_Center
print("Finding Game Client and re-sizing..")
find_target_client(char_name)

# Validating chat location for Socketing Success Task
print("Validating Chat UI integrity on screen..")
SystemChat = validate_chat()

# Setting chat to "System"
find_and_click_chat_button('system')

# Opening Shop & Mapping coordinates
mapping_inventory_and_shop()

# Opening Warehouse & Map coordinates
mapping_warehouse()

print("Adding Stop hotkeys..")
keyboard.add_hotkey('space', stop_script)  # Stop hotkey
keyboard.add_hotkey('shift+space', stop_script)  # Stop hotkey 2

time.sleep(1)  # Wait 1 second before starting

# Starting both threads
if __name__ == "__main__":
    print("Starting The Socketeer...")
    script_thread = threading.Thread(target=socketing_task)
    print("Starting Chat Parsing task...")
    image_processing_thread = threading.Thread(target=chat_parsing_task)
    print("Starting Coordinates Parsing task...")
    check_if_moved_thread = threading.Thread(target=check_if_moved)

    script_thread.start()
    image_processing_thread.start()
    check_if_moved_thread.start()

    script_thread.join()
    image_processing_thread.join()
    check_if_moved_thread.join()
    print("All Scripts have stopped.")
