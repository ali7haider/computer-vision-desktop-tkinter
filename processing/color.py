"""Color operations on uint8 grayscale or OpenCV BGR images."""

import cv2
import numpy as np

from utils.validators import validate_number


def grayscale(image):
    if image.ndim == 2:
        return image.copy()
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def brightness_contrast(image, brightness=0, contrast=1):
    brightness = validate_number(brightness, "Brightness", -255, 255)
    contrast = validate_number(contrast, "Contrast", 0, 3)
    # Float arithmetic avoids uint8 overflow; negative results must clip to zero.
    result = image.astype(np.float32) * contrast + brightness
    return np.clip(np.rint(result), 0, 255).astype(np.uint8)


def rgb_channels(image, red=1, green=1, blue=1):
    red = validate_number(red, "Red", 0, 2)
    green = validate_number(green, "Green", 0, 2)
    blue = validate_number(blue, "Blue", 0, 2)
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # OpenCV stores channels in blue, green, red order.
    gains = np.array([blue, green, red], dtype=np.float32)
    result = image.astype(np.float32) * gains
    return np.clip(np.rint(result), 0, 255).astype(np.uint8)
