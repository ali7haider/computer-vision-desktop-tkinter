"""Threshold masks and contour overlays for uint8 grayscale or BGR images."""

import cv2

from processing.color import grayscale
from utils.validators import validate_kernel_size, validate_number


def global_threshold(image, threshold=127):
    threshold = validate_number(threshold, "Threshold", 0, 255)
    _, mask = cv2.threshold(grayscale(image), threshold, 255, cv2.THRESH_BINARY)
    return mask


def adaptive_threshold(image, block_size=11, constant=2, method="Gaussian"):
    block = validate_kernel_size(block_size, name="Block size")
    constant = validate_number(constant, "Constant", -50, 50)
    methods = {"Mean": cv2.ADAPTIVE_THRESH_MEAN_C, "Gaussian": cv2.ADAPTIVE_THRESH_GAUSSIAN_C}
    if method not in methods:
        raise ValueError("Method must be Mean or Gaussian.")
    return cv2.adaptiveThreshold(
        grayscale(image), 255, methods[method], cv2.THRESH_BINARY, block, constant,
    )


def detect_contours(image, threshold=127):
    mask = global_threshold(image, threshold)
    # Show outer boundaries of bright foreground regions; holes are not outlined.
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if image.ndim == 2 else image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)
    return result
