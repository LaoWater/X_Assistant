import os
import time
import pyautogui
import cv2
import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Now import module
from automation_engine import find_image

hp_bar_path = r"hp_bar_template.png"

template = cv2.imread(hp_bar_path)

# The desired dimensions (width=55, height=9)
self_hp_bar_width = 52
self_hp_bar_height = 5

# Resize the image to the desired size
resized_template = cv2.resize(template, (self_hp_bar_width, self_hp_bar_height))

time.sleep(1)

# Save the resized image as "hp_bar_template.png"
output_path = "hp_bar_template.png"
cv2.imwrite(output_path, resized_template)


first_hp_bar = find_image(output_path, 0.9)
print(first_hp_bar)
pyautogui.moveTo(first_hp_bar)