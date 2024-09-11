import time
from pynput.mouse import (Listener)
import pyautogui
import pygetwindow as gw


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")
        # File writing
        # with open("mouse_coordinates.txt", "a") as file:
        # file.write(f"{x}, {y}\n")


def main():
    # Sleep for 2 seconds before starting the listener
    # Get the currently active window
    active_window = gw.getActiveWindow()

    # Check if there is an active window
    if active_window:
        # Get the window's position and size
        left, top = active_window.topleft
        width, height = active_window.size

        # Calculate the center position
        center_x = left + width // 2
        center_y = top + height // 2

        print(f"The center position of the current active window is at (X: {center_x}, Y: {center_y}).")

        time.sleep(0.8)
        # Optionally, move the mouse to the center of the active window
        pyautogui.moveTo(319, 305)
        time.sleep(1)
        # 10-Mar-2024
        # absolute right move x =994, y= 551 ->
        # absolute left move x =927, y= 551 ->
        # absolute down move x = 960, y= 567 ->
        # absolute up move x = 960, y= 534 ->
    else:
        print("No active window found.")

    time.sleep(2)
    print("Starting mouse click listener. Click somewhere to log coordinates.")

    # Start listening to mouse clicks
    with Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    main()

# Autolvler close char mouse taps
# Left : Mouse clicked at (897, 527)
# Up-Left: Mouse clicked at (911, 519)
# Up-Right: Mouse clicked at (1005, 513)
# Right: Mouse clicked at (1013, 545)
# Up: Mouse clicked at (953, 528)
# Down: Mouse clicked at (947, 576)
# Down-Left: Mouse clicked at (916, 559)
# Down-Right: Mouse clicked at (990, 573)