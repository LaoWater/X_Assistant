import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import TesseractError
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def color_matches(color1, color2, tolerance=10):
    """Check if two colors match within a given tolerance."""
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))


def show_color_swatch(color):
    """Create and display a color swatch for the given RGB color."""
    # Create a 100x100x3 array filled with the RGB color
    # Create a color swatch
    swatch = np.zeros((200, 200, 3), dtype=int)
    swatch[:, :] = color  # Set every pixel in the swatch to the selected color

    # Display the color swatch
    plt.imshow(swatch)
    plt.axis('off')  # Hide axes for better visual representation
    plt.show()


def get_pixel_color(image, x, y):
    """Get the color of the pixel from a PIL image at the given x,y coordinates."""
    return image.getpixel((x, y))


def resize_image(image_path, adjustment_factor):
    if True:
        with Image.open(image_path) as original_img:  # Renamed to avoid shadowing
            new_width = int(original_img.width * adjustment_factor)
            new_height = int(original_img.height * adjustment_factor)
            new_size = (new_width, new_height)
            resized_img = original_img.resize(new_size, Image.LANCZOS)
            # Consider saving to a new path instead of overwriting the original image
            resized_img.save("new_image_path.jpg")


def read_text_from_image(image):
    try:
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use color filtering if needed to isolate yellow text
        # Define range of yellow color in HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow_text = cv2.bitwise_and(gray, gray, mask=mask)

        # Apply thresholding to create a binary image
        _, binary = cv2.threshold(yellow_text, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Invert the image if necessary
        inverted_binary = cv2.bitwise_not(binary)

        # Use OCR to read the text
        text = pytesseract.image_to_string(inverted_binary, config='--psm 6')

        return text

    except Exception as e:
        # Handle any exceptions that occur and return a meaningful error message
        print(f"An error occurred: {e}")
        return None


def preprocess_for_ocr_hp(processed_img):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(processed_img, cv2.COLOR_BGR2HSV)

    # Define the range for strong red colors
    # These values might need to be adjusted based on your specific images
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine masks for red color
    red_mask = mask1 + mask2

    # Invert the mask to make red areas black and non-red areas white
    inverted_mask = cv2.bitwise_not(red_mask)
    # cv2.imshow('Inverted Mask', inverted_mask)

    # Apply the inverted mask to the grayscale image
    gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    highlighted_text = cv2.bitwise_and(gray, gray, mask=inverted_mask)
    # cv2.imshow('Highlighted Text', highlighted_text)

    # Binarize the image
    _, binarized = cv2.threshold(highlighted_text, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('Binarized', binarized)

    # Scale image (optional based on your requirement)
    scale_percent = 150  # percent of original size
    width = int(binarized.shape[1] * scale_percent / 100)
    height = int(binarized.shape[0] * scale_percent / 100)
    dim = (width, height)
    scaled = cv2.resize(binarized, dim, interpolation=cv2.INTER_LINEAR)
    # cv2.imshow('Scaled', scaled)

    return scaled  # This image is now ready for OCR processing


def preprocess_for_ocr(processed_img):
    # Isolate the red channel
    red_channel = processed_img[:, :, 2]

    # Convert the red channel to grayscale
    gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)

    # Subtract the grayscale from the isolated red channel
    diff = cv2.absdiff(red_channel, gray)

    # Normalize the result
    norm_diff = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # Apply a binary threshold to the normalized difference
    _, binarized = cv2.threshold(norm_diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('Binarized', binarized)

    # Scale image
    scale_percent = 150  # percent of original size
    width = int(processed_img.shape[1] * scale_percent / 100)
    height = int(processed_img.shape[0] * scale_percent / 100)
    dim = (width, height)
    scaled = cv2.resize(norm_diff, dim, interpolation=cv2.INTER_LINEAR)
    # cv2.imshow('Scaled', scaled)

    return scaled  # So far the best approach - 99% accuracy


def extract_text_from_image(processed_img):
    try:
        # Preprocess the image for OCR
        processed_img = preprocess_for_ocr(processed_img)

        # Use Tesseract OCR to extract text
        text = pytesseract.image_to_string(processed_img, lang='eng')

    except TesseractError as e:
        # Handle Tesseract error
        print(f"An error occurred with Tesseract OCR: {e}")
        text = "System Chat not read-able\nTrying Again.."  # Default text to handle error

    except Exception as e:
        # Handle other potential errors (e.g., during preprocessing)
        print(f"An unexpected error occurred: {e}")
        text = "System Chat not read-able\nTrying Again.."  # Default text to handle error

    return text


def extract_text_from_image_hp(processed_img):
    # Preprocess the image for OCR
    processed_img = preprocess_for_ocr_hp(processed_img)

    # Use Tesseract OCR to extract text
    text = pytesseract.image_to_string(processed_img, lang='eng')

    return text
