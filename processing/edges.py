"""Binary edge maps from uint8 grayscale or BGR images."""

import cv2
import numpy as np

from processing.color import grayscale
from utils.validators import validate_edge_size, validate_number


def sobel_edges(image, kernel_size=3, mean_ratio=1):
    kernel = validate_edge_size(kernel_size, "Kernel size")
    ratio = validate_number(mean_ratio, "Mean ratio", 0, 10)
    gray = grayscale(image)
    # Signed derivatives preserve both dark-to-light and light-to-dark edges.
    horizontal = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel)
    vertical = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel)
    magnitude = np.hypot(horizontal, vertical)
    threshold = ratio * magnitude.mean()
    # Strict comparison keeps constant images black even when the mean is zero.
    return (magnitude > threshold).astype(np.uint8) * 255


def canny_edges(image, threshold_1=100, threshold_2=200, aperture_size=3):
    low = validate_number(threshold_1, "Threshold 1", 0, 255)
    high = validate_number(threshold_2, "Threshold 2", 0, 255)
    aperture = validate_edge_size(aperture_size, "Aperture size")
    if low > high:
        raise ValueError("Threshold 1 must be less than or equal to Threshold 2.")
    return cv2.Canny(grayscale(image), low, high, apertureSize=aperture)
