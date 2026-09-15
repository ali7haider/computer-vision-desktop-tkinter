# Project Overview

## Product / Project Name

**Interactive Computer Vision Tool with GUI**

A standalone desktop computer vision application developed using **Python, OpenCV, and Tkinter**.

---

## Purpose

The purpose of this project is to build a small interactive computer vision application that demonstrates practical understanding of:

* Image loading and saving
* Image processing
* Computer vision operations
* Interactive parameter adjustment
* Tkinter GUI development
* Webcam integration
* Input validation
* Safe application behavior

The project is an **academic application**, not a production or commercial product.

The implementation should therefore prioritize **correctness, simplicity, readability, stability, and understanding** rather than production-level architecture.

---

## Problem

Computer vision operations are often demonstrated using separate scripts with hardcoded images and parameters.

This project combines multiple operations into one interactive desktop application where a user can:

1. Load an image or capture one from a webcam.
2. Select a computer vision operation.
3. Adjust its parameters.
4. Immediately observe the result.
5. Save the processed image.

The application must also safely handle invalid user actions and parameter values instead of crashing.

---

## Users / Consumers

The primary users are:

### Student

The student develops, demonstrates, documents, and explains the application.

The student must understand the implementation and be able to explain the code and modify parameters during evaluation.

### Instructor / Evaluator

The instructor will evaluate the application based on:

* Required functionality
* Correct implementation
* GUI usability
* Parameter controls
* Stability
* Code organization
* Documentation
* Student understanding

The instructor may run the application locally from the terminal and interact with different features and parameters.

---

## Core Capabilities

The application must provide the following core capabilities.

### Image Input

* Open images from the local computer.
* Support JPG, PNG, and BMP at minimum.
* Display the selected image inside the GUI.

### Webcam

* Access the system webcam.
* Display the live webcam feed.
* Allow the user to take a snapshot.
* Stop the webcam after taking a snapshot.
* Use the snapshot as a normal image for further processing.

### Image Processing

Provide at least **10 image-processing/computer-vision operations** while satisfying the required assignment categories:

* Foundations & Color
* Image Statistics
* Point & Local Operators
* Edge Detection
* Segmentation

### Interactive Parameters

Operations should expose appropriate parameters through:

* Sliders / trackbars
* Textboxes
* Buttons
* Menu actions

Changes should update the displayed result interactively where appropriate.

### Image Output

* Display the processed result.
* Save the currently displayed result using **File → Save As...**

### Safe User Interaction

The application must safely handle:

* No image loaded
* Invalid numeric input
* Invalid parameter ranges
* Invalid kernel sizes
* Unsupported/unreadable images
* Webcam unavailable
* Webcam frame failure
* Cancelled file dialogs
* Operations used in an incorrect state

These situations must not cause the application to crash.

---

# Scope

## In Scope

The project includes:

* Python desktop application
* Tkinter GUI
* OpenCV image processing
* NumPy where required for image operations
* Local image loading
* Local image saving
* Webcam access
* Webcam snapshot
* Menu bar
* Buttons
* Sliders / trackbars
* Numeric text input
* Parameter validation
* User-friendly warnings/errors
* At least 10 required image-processing operations
* Histogram display
* Real-time parameter adjustment where appropriate
* Proper camera/resource cleanup
* Clean application exit
* Simple modular project structure
* Code comments where useful
* PDF documentation
* GUI screenshots
* Demo video

---

## Out of Scope

The following are intentionally outside the scope of this project:

* Web application
* Mobile application
* Cloud deployment
* Google Colab execution
* PyQt
* Web frameworks
* Backend/API
* Database
* Authentication
* User accounts
* Cloud image storage
* Remote image processing
* Distributed processing
* Production monitoring
* Complex logging systems
* Plugin architecture
* Enterprise design patterns
* Advanced dependency injection
* Microservices
* Production deployment infrastructure

Features should not be added simply to make the application appear more sophisticated.

---

# Major Modules

## Application Coordinator

**File:** `app.py`

Responsible for coordinating the application.

Main responsibilities:

* Maintain application state
* Maintain current/base image
* Maintain displayed/processed image
* Connect GUI actions to processing functions
* Coordinate webcam state
* Coordinate image updates
* Handle application shutdown

---

## GUI

**Folder:** `gui/`

Responsible for presenting and controlling the user interface.

### `layout.py`

Responsible for:

* Main window structure
* Menu structure
* Image display area
* General GUI layout

### `controls.py`

Responsible for:

* Buttons
* Sliders
* Trackbars
* Textboxes
* Parameter controls
* Snapshot controls

GUI files should not contain the actual computer-vision algorithms.

---

## Core

**Folder:** `core/`

Responsible for non-processing application functionality.

### `file_handler.py`

Responsible for:

* Opening images
* Loading images
* Saving processed images
* Handling invalid/unreadable files

### `webcam.py`

Responsible for:

* Opening webcam
* Reading frames
* Checking webcam availability
* Stopping webcam
* Releasing webcam resources
* Supporting snapshot capture

---

## Processing

**Folder:** `processing/`

Contains the computer-vision and image-processing operations.

### `color.py`

Color and foundation operations such as:

* RGB channel manipulation
* Grayscale
* Brightness / contrast
* HSV adjustment

### `statistics.py`

Image statistics:

* Histogram computation/display
* Histogram equalization

### `filters.py`

Point and local operations such as:

* Median filtering
* Gaussian smoothing
* Contrast stretching
* Sharpening

### `edges.py`

Edge detection operations such as:

* Sobel
* Canny
* Laplacian of Gaussian

### `segmentation.py`

Segmentation operations such as:

* Global thresholding
* Adaptive thresholding
* Contour detection

Only the operations selected for the final application need to be implemented.

---

## Validation

**File:** `utils/validators.py`

Responsible for reusable parameter validation.

Examples:

* Numeric validation
* Kernel-size validation
* Odd-number validation
* Parameter range validation
* Safe/default parameter handling

Validation should prevent invalid values from reaching OpenCV functions where they could cause runtime errors.

---

# Technology

The project uses:

* **Python**
* **OpenCV**
* **Tkinter**
* **NumPy**

Additional libraries should only be introduced when genuinely necessary for satisfying the assignment.

The application must run locally from the terminal.

```bash
python main.py
```

---

# Design Principles

## 1. Simplicity First

Choose the simplest implementation that correctly satisfies the requirement.

Avoid introducing abstractions simply because they would be appropriate in a larger production application.

---

## 2. No-Crash Principle

The application should remain running when expected errors occur.

The general pattern is:

```text
User Action
    ↓
Check Application State
    ↓
Validate Input
    ↓
Execute Operation
    ↓
Display Result
```

For invalid input:

```text
Invalid Action / Parameter
    ↓
Handle Safely
    ↓
Show Message or Use Safe Default
    ↓
Return
    ↓
Application Continues
```

A user mistake should not terminate the program.

---

## 3. Clear Responsibilities

Each module should have one clear purpose.

For example:

```text
GUI
 ↓
Application Coordinator
 ↓
Processing / Core
```

Processing functions should not be responsible for creating Tkinter widgets.

GUI modules should not contain complex image-processing implementations.

---

## 4. Understandable Code

Code must be understandable by the student.

Prefer straightforward functions such as:

```python
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

over unnecessary generic abstractions.

The student should be able to explain what each major function does during evaluation.

---

## 5. Validate Before Processing

Parameters that could cause OpenCV errors should be checked before executing the operation.

Examples include:

* Kernel sizes
* Thresholds
* Sigma values
* Aperture sizes
* Numeric textbox values

---

## 6. Develop Incrementally

Features should be implemented and tested individually before being combined.

Do not build every operation first and wait until the end to test the complete application.

---

# Important Constraints

The following constraints must be respected throughout development.

### Technology

* Python only.
* OpenCV + Tkinter for the application.
* No PyQt.
* No web framework.
* Must run locally.
* Must be executable from the terminal.

### Functionality

At least **10 image-processing/vision operations** must be implemented while satisfying the required category minimums.

Histogram computation and histogram equalization are required.

### Structure

The application must use functions/classes and should not become one giant script.

At the same time, the architecture should remain appropriate for a small academic project.

### Stability

The application must handle edge cases safely.

**Under expected user interactions, the application should not crash.**

Invalid input should result in:

* A helpful message, or
* A safe/default parameter where appropriate.

### Academic Understanding

AI assistance may be used, but generated code must be understood and explainable by the student.

Complexity that makes the implementation difficult to explain should be avoided.

---

# Non-Goals

This project is **not intended to demonstrate production software architecture**.

We are not optimizing for:

* Large development teams
* Millions of users
* Scalability
* Cloud infrastructure
* Long-term production maintenance
* Enterprise architecture
* Maximum abstraction
* Maximum number of features

We are optimizing for:

**Correctness + Stability + Simplicity + Understanding + Assignment Compliance**

---

# Success Criteria

The project is considered successful when:

1. The application launches successfully from the terminal.

2. A user can open JPG, PNG, and BMP images.

3. A user can access the webcam.

4. A user can take a webcam snapshot and continue processing it.

5. At least 10 computer-vision/image-processing operations are correctly implemented.

6. Required operation categories are satisfied.

7. Histogram computation and histogram equalization are implemented.

8. Required parameters can be controlled through appropriate GUI controls.

9. Interactive parameters update the image appropriately.

10. The currently displayed processed image can be saved.

11. Invalid parameters are handled safely.

12. Running an operation without an image is handled safely.

13. Webcam failures are handled safely.

14. Cancelling Open/Save dialogs does not cause errors.

15. Webcam resources are released correctly.

16. The application exits cleanly.

17. The project remains organized according to the agreed folder structure.

18. The implementation is readable and understandable.

19. The student can explain the major components and image-processing operations.

20. The PDF documentation contains the required descriptions, parameters, screenshots, and demo link.

21. The demo video successfully demonstrates the required workflow.

22. Normal and invalid user interactions do not cause the application to crash.

---

# Guiding Principle

When choosing between two implementations, prefer the one that is:

1. **Correct**
2. **Stable**
3. **Simple**
4. **Easy to understand**
5. **Easy to explain**

Do not add complexity unless it directly helps satisfy an assignment requirement.
