"""Grayscale intensity statistics and histogram equalization."""

import cv2

from processing.color import grayscale


def compute_histogram(image):
    """Return pixel counts for all 256 grayscale intensity levels."""
    gray = grayscale(image)
    return cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()


def equalize_histogram(image):
    """Equalize grayscale intensities; the returned image is grayscale."""
    return cv2.equalizeHist(grayscale(image))
