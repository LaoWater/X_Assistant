import os
from PIL import Image

# Images Path
# Define the base path for images
image_base_path = 'Images'

# Using os.path.join to construct file paths
hpbar_path = os.path.join(image_base_path, 'hp_image.PNG')
try:
    img = Image.open(hpbar_path)
    # Proceed with your image processing
except FileNotFoundError:
    print(f"Error: '{hpbar_path}' not found in the specified directory.")

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
