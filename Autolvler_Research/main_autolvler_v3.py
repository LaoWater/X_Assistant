import os
import time
import pyautogui
import cv2
from automation_engine import find_image

hp_bar_path = r"C:\Users\baciu\Desktop\Neo\Conquer World\Auto_Lvler_Images\V2 - Prestige\full_hp_bar.png"

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