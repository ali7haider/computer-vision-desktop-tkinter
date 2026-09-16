"""Validate numeric parameters before image processing."""

import math


def validate_number(value, name, minimum, maximum):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number.") from None
    if not math.isfinite(number) or not minimum <= number <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")
    return number


def validate_kernel_size(value):
    """Limit filter kernels to useful, positive odd integers."""
    text = str(value).strip()
    if not text.isascii() or not text.isdecimal():
        raise ValueError("Kernel size must be an odd integer from 3 to 31.")
    if len(text) > 2:
        raise ValueError("Kernel size must be an odd integer from 3 to 31.")
    kernel = int(text)
    if not 3 <= kernel <= 31 or kernel % 2 == 0:
        raise ValueError("Kernel size must be an odd integer from 3 to 31.")
    return kernel
