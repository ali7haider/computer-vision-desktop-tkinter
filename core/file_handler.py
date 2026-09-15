"""Read and write image files independently of the GUI."""

from pathlib import Path

import cv2
import numpy as np


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def validate_extension(path):
    extension = Path(path).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Choose a JPG, PNG, or BMP image file.")
    return extension


def load_image(path):
    validate_extension(path)
    # Read through NumPy to support paths containing Unicode characters.
    data = np.fromfile(path, dtype=np.uint8)
    if data.size == 0:
        raise ValueError("The selected file is empty.")
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The selected file is not a readable image.")
    return image


def save_image(path, image):
    extension = validate_extension(path)
    # Encode before opening the destination so encoding failures cannot erase it.
    success, encoded = cv2.imencode(extension, image)
    if not success:
        raise ValueError("The image could not be encoded for saving.")
    encoded.tofile(path)
