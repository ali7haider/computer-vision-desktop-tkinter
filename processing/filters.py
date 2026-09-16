"""Local filters for uint8 grayscale and BGR images."""

import cv2
import numpy as np

from utils.validators import validate_kernel_size, validate_number


def median_filter(image, kernel_size=3):
    kernel = validate_kernel_size(kernel_size)
    return cv2.medianBlur(image, kernel)


def gaussian_smoothing(image, kernel_size=5, sigma=0):
    kernel = validate_kernel_size(kernel_size)
    sigma = validate_number(sigma, "Sigma", 0, 10)
    # Sigma zero asks OpenCV to derive it from the kernel size.
    return cv2.GaussianBlur(image, (kernel, kernel), sigmaX=sigma)


def sharpen(image):
    # Center minus its four neighbors emphasizes local intensity differences.
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    return cv2.filter2D(image, -1, kernel)
