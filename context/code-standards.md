# Code Standards

## General Principles

Code should be:

* Simple
* Readable
* Correct
* Easy to explain
* Consistent
* Safe against expected user errors

This is an academic project. Do not introduce production-level complexity unless it is necessary for an assignment requirement.

Prefer straightforward Python over clever abstractions.

---

## Language / Runtime

* Language: **Python**
* Computer Vision: **OpenCV**
* GUI: **Tkinter**
* Image/Data operations: **NumPy**
* Run locally from the terminal.

```bash
python main.py
```

Do not use PyQt, web frameworks, or Google Colab.

---

## Project Structure

Follow the agreed structure:

```text
ComputerVisionApp/
│
├── main.py
├── app.py
├── gui/
├── core/
├── processing/
├── utils/
└── README.md
```

Do not create new folders or architectural layers without a clear reason.

---

## File Organization

Keep responsibilities separated:

```text
main.py                 → Application startup
app.py                  → Application coordination/state

gui/                    → GUI
core/                   → Files and webcam
processing/             → Image-processing algorithms
utils/validators.py     → Validation
```

Do not put unrelated responsibilities into the same file.

---

# Naming Conventions

Use normal Python naming conventions.

## Files

Use lowercase `snake_case`.

```text
file_handler.py
webcam.py
color.py
statistics.py
```

## Variables

Use descriptive `snake_case`.

```python
current_image
processed_image
kernel_size
threshold_value
```

Avoid unclear names such as:

```python
x1
temp2
thing
data123
```

unless short names such as `x`, `y`, or `k` are meaningful in the algorithm.

## Functions

Use descriptive `snake_case`.

```python
open_image()
save_image()
apply_median_filter()
validate_kernel_size()
```

## Classes / Components

Use `PascalCase`.

```python
ComputerVisionApp
WebcamManager
```

Only create classes when they provide a clear benefit.

## Constants

Use uppercase `SNAKE_CASE`.

```python
DEFAULT_KERNEL_SIZE = 3
MAX_THRESHOLD = 255
```

## Types / Interfaces

No complex type system or interface architecture is required.

Simple Python type hints may be used where they improve readability.

---

# Functions

Functions should:

* Have one clear responsibility
* Use meaningful names
* Remain reasonably small
* Return results instead of changing unrelated state
* Be easy to understand

Processing functions should generally follow:

```python
def gaussian_blur(image, kernel_size, sigma):
    ...
    return processed_image
```

Avoid very large functions that handle GUI, validation, processing, and file operations together.

---

# Types

Type hints are optional but encouraged where they make code easier to understand.

Example:

```python
def validate_kernel_size(value: int) -> int:
    ...
```

Do not introduce complicated custom typing purely for architecture.

---

# Imports / Exports

Keep imports clear and grouped.

Example:

```python
import cv2
import numpy as np
import tkinter as tk

from tkinter import filedialog, messagebox
```

Avoid wildcard imports:

```python
from module import *
```

Avoid circular imports between modules.

---

# Error Handling

Expected user mistakes must **not crash the application**.

Handle situations such as:

* No image loaded
* Invalid parameter
* Invalid file
* Webcam unavailable
* Webcam read failure
* Save failure
* Cancelled dialogs

Use clear Tkinter messages where appropriate.

Example:

```python
if image is None:
    messagebox.showwarning(
        "No Image",
        "Please load an image first."
    )
    return
```

Do not silently ignore important errors.

---

# Validation

Validate parameters **before passing them to OpenCV**.

Examples:

* Kernel size
* Odd/even requirements
* Threshold range
* Sigma
* Aperture size
* Numeric textbox values

When appropriate:

```text
Invalid value
     ↓
Show message or use safe default
     ↓
Continue application
```

Validation should be simple and predictable.

---

# API Conventions

Not applicable.

This project has no backend or external API.

---

# Data Access

No database is used.

Images are:

* Loaded from the local filesystem
* Held in memory
* Saved to the local filesystem

---

# State Management

Application state should primarily be coordinated through `app.py`.

Typical state includes:

```python
current_image
display_image
webcam_running
latest_frame
```

Do not introduce a separate state-management framework.

---

# Logging

No logging framework is required.

Simple console messages may be used during development.

User-facing errors should normally use Tkinter dialogs.

---

# Security

No production security system is required.

Basic rules:

* Validate user input
* Do not execute user-provided text as code
* Handle files safely
* Release webcam resources

---

# Testing

Each feature should be manually tested after implementation.

At minimum test:

* Normal usage
* No image loaded
* Invalid parameters
* Boundary parameter values
* Cancelled dialogs
* Webcam unavailable
* Save failures where possible
* Clean application exit

The main rule is:

> Invalid user interaction should not crash the application.

---

# Documentation

Keep documentation focused on:

* What the function does
* Important parameters
* Important constraints
* Non-obvious computer-vision logic

Avoid unnecessary long documentation for obvious code.

---

# Comments

Use comments to explain **why**, especially for computer-vision logic.

Good:

```python
# Gaussian kernels must use positive odd dimensions.
```

Avoid comments that simply repeat the code.

Bad:

```python
# Set kernel size to 5
kernel_size = 5
```

---

# Formatting / Linting

Follow standard Python formatting.

General rules:

* 4 spaces for indentation
* Reasonable line lengths
* Blank lines between logical sections
* Consistent formatting
* No unnecessary trailing code or commented-out blocks

No complicated linting setup is required.

---

# Dependency Rules

Keep dependencies minimal.

Preferred dependencies:

```text
opencv-python
numpy
```

Tkinter should be used for the GUI.

Only add another dependency when it is genuinely required.

Dependency direction should remain:

```text
GUI
 ↓
APP
 ↓
CORE / PROCESSING
```

Processing code should not depend on GUI code.

---

# Performance Guidelines

No advanced optimization is required.

However:

* Avoid unnecessary image copies
* Avoid repeatedly loading the same image from disk
* Keep webcam updates non-blocking
* Resize images for GUI preview when necessary
* Avoid expensive processing on every frame unless required

Correctness and readability are more important than micro-optimization.

---

# Forbidden Patterns

Avoid:

* One giant Python file
* Giant functions
* Unnecessary inheritance
* Deep class hierarchies
* Excessive abstraction
* Unnecessary design patterns
* Global mutable state where avoidable
* Circular imports
* Wildcard imports
* Empty `except:` blocks
* Ignoring errors that can cause crashes
* Hardcoded local file paths
* Mixing processing algorithms directly into GUI layout code
* Adding dependencies without a clear need
* Creating new folders for individual small functions

Do not overengineer the project.

---

# Exceptions

These standards are guidelines for keeping the project consistent.

A rule may be changed when:

1. An assignment requirement demands it.
2. OpenCV/Tkinter requires a different approach.
3. The alternative clearly makes the implementation simpler or safer.

When uncertain, choose the solution that is:

**simpler, safer, easier to understand, and easier to explain.**
