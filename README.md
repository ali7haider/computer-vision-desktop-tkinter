# Computer Vision App — Full Development Plan

## 1. Project Goal

Build a **standalone desktop Computer Vision application** using **Python, OpenCV, and Tkinter**.

The application will allow the user to:

* Open local images
* Access the live webcam
* Take a webcam snapshot
* Apply multiple image-processing and computer-vision operations
* Adjust operation parameters interactively
* Preview results
* Reset the image
* Save the processed output
* Handle invalid input and common edge cases without crashing

The application will remain **simple and academic**, not production-level software. However, we will still follow good coding practices such as separating responsibilities into folders/modules, keeping functions small, avoiding global state, validating input, and releasing webcam resources correctly.

The assignment requires structured Python code rather than one giant script, while using OpenCV and Tkinter and running locally from the terminal.

---

# 2. Development Philosophy

We will follow this principle:

> Simple implementation + clean structure + understandable code + full assignment compliance.

We will avoid unnecessary complexity.

We will use:

* Python
* OpenCV
* Tkinter
* Standard Python libraries where required
* One main application class
* Separate processing modules
* Simple helper functions
* Straightforward validation
* Simple GUI callbacks

We will NOT introduce:

* Database
* Backend/API
* Authentication
* Web framework
* Docker
* Dependency injection
* Repository pattern
* Plugin architecture
* Complex MVC framework
* Undo/redo engine
* Complex threading
* Production logging systems
* Cloud services
* Machine-learning models

The goal is that every file and function should be easy to understand and explain during the technical interview.

---

# 3. Final Project Structure

```text
ComputerVisionApp/
│
├── main.py
├── app.py
│
├── gui/
│   ├── __init__.py
│   ├── layout.py
│   └── controls.py
│
├── core/
│   ├── __init__.py
│   ├── file_handler.py
│   └── webcam.py
│
├── processing/
│   ├── __init__.py
│   ├── color.py
│   ├── statistics.py
│   ├── filters.py
│   ├── edges.py
│   └── segmentation.py
│
├── utils/
│   ├── __init__.py
│   └── validators.py
│
└── README.md
```

---

# 4. High-Level Architecture

```text
                    USER
                     │
                     ▼
                    GUI
                     │
                     ▼
                  app.py
                /    |    \
               /     |     \
              ▼      ▼      ▼
          File      Webcam   Processing
          Core       Core
               \     |     /
                \    |    /
                     ▼
               current_image
                     │
                     ▼
                    GUI
```

The GUI collects user input.

`app.py` coordinates the application.

Processing modules receive an image and parameters and return a processed image.

The GUI then displays the returned result.

---

# 5. `main.py`

`main.py` is only the application entry point.

Conceptually:

```python
import tkinter as tk
from app import ComputerVisionApp

root = tk.Tk()
app = ComputerVisionApp(root)
root.mainloop()
```

Responsibilities:

```text
Create Tkinter root
        ↓
Create application
        ↓
Start event loop
```

Nothing else should be placed here.

---

# 6. `app.py`

This contains the main application class:

```python
class ComputerVisionApp:
    ...
```

It coordinates:

* GUI
* Application state
* File handling
* Webcam
* Processing operations
* Reset functionality
* Apply functionality
* Snapshot handling
* Application cleanup

Main state:

```python
self.original_image
self.current_image
self.operation_source

self.current_operation

self.webcam
self.webcam_active
self.current_frame
```

`app.py` should coordinate operations but should not contain all OpenCV algorithms.

---

# 7. Image State

We will maintain three important image variables.

```python
self.original_image
self.current_image
self.operation_source
```

### `original_image`

The originally opened image or webcam snapshot.

Used when the user selects:

```text
Reset Image
```

### `current_image`

The current processed result.

This is also the image saved using **Save As**.

### `operation_source`

A temporary copy used when interactively adjusting parameters.

Example:

```text
Current Image
      ↓
Select Gaussian Blur
      ↓
operation_source = current_image.copy()
      ↓
Move sigma slider
      ↓
Always process operation_source
```

This prevents repeated slider movements from processing an already blurred image again and again.

---

# 8. Main Application Flow

```text
Launch Application
        │
        ▼
Empty GUI
        │
        ├───────────────┐
        │               │
        ▼               ▼
Open Image          Open Webcam
        │               │
        │          Live Video
        │               │
        │         Take Snapshot
        │               │
        └───────┬───────┘
                ▼
          Static Image
                │
                ▼
       Select Operation
                │
                ▼
       Show Parameters
                │
                ▼
      Adjust Parameters
                │
                ▼
        Preview Result
                │
                ▼
              Apply
                │
          ┌─────┴─────┐
          ▼           ▼
        Reset       Save As
```

---

# 9. Main GUI Layout

The interface will remain simple.

```text
┌──────────────────────────────────────────────────────────┐
│ File                       Tools                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│                                                          │
│                    IMAGE PREVIEW                         │
│                                                          │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Operation: Gaussian Smoothing                            │
│                                                          │
│ Kernel Size: [ 5 ]                                       │
│ Sigma:       ─────────●────────                          │
│                                                          │
│ [Apply]       [Reset Image]       [Take Snapshot]        │
├──────────────────────────────────────────────────────────┤
│ Status: Image loaded                                     │
└──────────────────────────────────────────────────────────┘
```

The assignment specifically requires menus, buttons, sliders/trackbars and numeric text input.

---

# 10. File Menu

```text
File
├── Open Image...
├── Access Live Webcam
├── Save As...
├── Reset Image
└── Exit
```

The assignment requires local image opening, webcam input and output saving.

---

# 11. Tools Menu

```text
Tools
├── Foundations & Color
│   ├── Grayscale
│   ├── Brightness / Contrast
│   └── HSV Adjustment
│
├── Image Statistics
│   ├── Histogram
│   └── Histogram Equalization
│
├── Filters
│   ├── Median Filter
│   ├── Gaussian Smoothing
│   └── Sharpening
│
├── Edge Detection
│   ├── Sobel
│   └── Canny
│
└── Segmentation
    ├── Global Threshold
    └── Adaptive Threshold
```

Optional later:

```text
Contour Detection
```

---

# 12. `gui/layout.py`

Handles the main GUI layout.

Functions can include:

```text
create_menu()
create_layout()
create_image_area()
create_control_area()
create_status_bar()
display_image()
update_status()
```

Responsibilities:

* Create frames
* Create menu
* Create image preview area
* Create parameter panel
* Create action buttons
* Display images
* Update status text

It should contain GUI code, not OpenCV algorithms.

---

# 13. `gui/controls.py`

Handles operation-specific controls.

Functions can include:

```text
clear_controls()

show_grayscale_controls()
show_brightness_controls()
show_hsv_controls()

show_histogram_controls()

show_median_controls()
show_gaussian_controls()

show_sobel_controls()
show_canny_controls()

show_global_threshold_controls()
show_adaptive_threshold_controls()
```

Example:

Selecting:

```text
Tools → Edge Detection → Canny
```

changes the parameter area into:

```text
Canny Edge Detection

Threshold 1:
0 ─────────●──────── 255

Threshold 2:
0 ─────────────●──── 255

Aperture:
[ 3 ▼ ]

[Apply]
```

---

# 14. Image Display

Images may be larger than the application window.

We will resize images **only for preview**.

Example:

```text
Real processed image
1920 × 1080
      ↓
Preview resize
      ↓
900 × 500
```

Saving still saves:

```text
1920 × 1080
```

We should never overwrite the real processed image with the resized preview.

---

# 15. `core/file_handler.py`

Functions:

```text
open_image()
save_image()
```

Possible helper:

```text
is_supported_file()
```

Supported formats should include at least:

```text
JPG
JPEG
PNG
BMP
```

as required by the assignment.

---

# 16. Open Image Flow

```text
File → Open Image
        ↓
Tkinter file dialog
        ↓
cv2.imread()
        ↓
Return image
        ↓
original_image = image
current_image = image.copy()
        ↓
Display image
```

If an invalid image is selected:

```text
Unable to open the selected image.
```

The application should not crash.

---

# 17. Save Image Flow

```text
File → Save As
        ↓
Choose destination
        ↓
cv2.imwrite(current_image)
```

We save:

```python
self.current_image
```

not the original image.

The assignment specifically requires saving the currently displayed processed image.

---

# 18. Reset Image

Reset remains simple:

```python
self.current_image = self.original_image.copy()
```

Flow:

```text
Processed Result
      ↓
Reset Image
      ↓
Original Image
```

No undo/redo system is required.

---

# 19. `core/webcam.py`

Handles webcam resources.

Functions:

```text
start_webcam()
read_frame()
stop_webcam()
is_webcam_available()
```

Basic OpenCV call:

```python
cv2.VideoCapture(0)
```

We will use Tkinter's:

```python
root.after(...)
```

for updating webcam frames instead of introducing unnecessary threading.

---

# 20. Webcam Flow

```text
File
 ↓
Access Live Webcam
 ↓
start_webcam()
 ↓
VideoCapture(0)
 ↓
Read frame
 ↓
Display frame
 ↓
root.after(...)
 ↓
Read next frame
```

The assignment requires live webcam input.

---

# 21. Snapshot Flow

```text
Live Webcam
      ↓
Take Snapshot
      ↓
Copy current frame
      ↓
Stop webcam
      ↓
original_image = snapshot
      ↓
current_image = snapshot.copy()
      ↓
Display snapshot
      ↓
Static-image mode
```

The snapshot can then be processed exactly like a normal opened image.

---

# 22. Webcam Cleanup

When any of these happen:

```text
Take Snapshot
Open Image
Exit Program
Close Window
```

the webcam must be released if active.

Example:

```python
capture.release()
```

The assignment explicitly requires proper camera/resource cleanup.

---

# 23. Processing Scope

We will implement **12 primary operations**.

This gives us more than the minimum of 10 while satisfying every category requirement.

The assignment requires at least 10 total operations with minimum coverage across several categories.

---

# 24. Final Operation List

| #  | Category            | Operation              |
| -- | ------------------- | ---------------------- |
| 1  | Foundations & Color | Grayscale              |
| 2  | Foundations & Color | Brightness / Contrast  |
| 3  | Foundations & Color | HSV Adjustment         |
| 4  | Statistics          | Histogram              |
| 5  | Statistics          | Histogram Equalization |
| 6  | Local Operators     | Median Filter          |
| 7  | Local Operators     | Gaussian Smoothing     |
| 8  | Local Operators     | Sharpening             |
| 9  | Edge Detection      | Sobel                  |
| 10 | Edge Detection      | Canny                  |
| 11 | Segmentation        | Global Threshold       |
| 12 | Segmentation        | Adaptive Threshold     |

Optional:

```text
13. Contour Detection
```

---

# 25. `processing/color.py`

Functions:

```python
grayscale(image)

brightness_contrast(
    image,
    brightness,
    contrast
)

adjust_hsv(
    image,
    hue,
    saturation,
    value
)
```

The assignment requires at least two operations from the foundations/color group; we will implement three.

---

# 26. Grayscale

Function:

```python
grayscale(image)
```

Uses:

```python
cv2.cvtColor(...)
```

Flow:

```text
BGR Image
    ↓
Grayscale conversion
    ↓
Single-channel image
```

No parameters required.

---

# 27. Brightness / Contrast

Function:

```python
brightness_contrast(
    image,
    brightness,
    contrast
)
```

Controls:

```text
Brightness:
-100 ───────── 0 ───────── +100

Contrast:
0.5 ───────── 1.0 ───────── 3.0
```

Both will use sliders.

This is also useful for demonstrating real-time parameter adjustment.

---

# 28. HSV Adjustment

Function:

```python
adjust_hsv(
    image,
    hue,
    saturation,
    value
)
```

Controls:

```text
Hue
────────●────────

Saturation
────────●────────

Value
────────●────────
```

Flow:

```text
BGR
 ↓
HSV
 ↓
Adjust H/S/V
 ↓
Validate ranges
 ↓
HSV → BGR
```

---

# 29. `processing/statistics.py`

Functions:

```python
histogram(image, channel)

histogram_equalization(image)
```

Both are mandatory according to the assignment.

---

# 30. Histogram

Instead of introducing Matplotlib, we can keep the implementation based on OpenCV.

Flow:

```text
Image
 ↓
cv2.calcHist()
 ↓
Normalize histogram
 ↓
Create blank OpenCV image
 ↓
Draw graph using cv2.line()
 ↓
Display histogram
```

Control:

```text
Channel:
[ Grayscale ▼ ]
```

Possible values:

```text
Grayscale
Blue
Green
Red
```

---

# 31. Histogram Equalization

Function:

```python
histogram_equalization(image)
```

Simple flow:

```text
Image
 ↓
Convert to grayscale
 ↓
cv2.equalizeHist()
 ↓
Improved-contrast image
```

No parameters required.

---

# 32. `processing/filters.py`

Functions:

```python
median_filter(
    image,
    kernel_size
)

gaussian_blur(
    image,
    kernel_size,
    sigma
)

sharpen(image)
```

We only need two from this category, but we implement three.

---

# 33. Median Filter

Function:

```python
median_filter(image, kernel_size)
```

Control:

```text
Kernel Size:
[ 5 ]

[Apply]
```

Validation:

```text
Must be integer
Must be positive
Must be odd
```

Examples:

```text
3 ✓
5 ✓
7 ✓

4 ✗
0 ✗
-1 ✗
abc ✗
```

This also satisfies the requirement for validated numeric textbox input.

---

# 34. Gaussian Smoothing

Function:

```python
gaussian_blur(
    image,
    kernel_size,
    sigma
)
```

Controls:

```text
Kernel Size:
[ 5 ]

Sigma:
0 ───────●──────── 10

[Apply]
```

The assignment specifically expects Gaussian smoothing to expose kernel size and sigma.

---

# 35. Sharpening

Function:

```python
sharpen(image)
```

Use a simple sharpening kernel such as:

```text
 0  -1   0
-1   5  -1
 0  -1   0
```

and process using:

```python
cv2.filter2D()
```

No parameter is required.

---

# 36. `processing/edges.py`

Functions:

```python
sobel(
    image,
    kernel_size,
    threshold_ratio
)

canny(
    image,
    threshold1,
    threshold2,
    aperture_size
)
```

The assignment requires at least two edge-detection methods.

---

# 37. Sobel

Controls:

```text
Kernel Size:
[ 3 ▼ ]

Threshold Ratio:
0.1 ─────────●──────── 3.0

[Apply]
```

Flow:

```text
Image
 ↓
Grayscale
 ↓
Sobel X
 ↓
Sobel Y
 ↓
Gradient magnitude
 ↓
Calculate mean gradient
 ↓
Threshold = mean × ratio
 ↓
Edge image
```

This follows the assignment requirement for kernel size and threshold based on a ratio of the mean.

---

# 38. Canny

Function:

```python
canny(
    image,
    threshold1,
    threshold2,
    aperture_size
)
```

Controls:

```text
Threshold 1
0 ─────────●──────── 255

Threshold 2
0 ─────────────●──── 255

Aperture:
[ 3 ▼ ]

[Apply]
```

Allowed aperture values:

```text
3
5
7
```

The assignment specifically mentions these controls for Canny.

---

# 39. `processing/segmentation.py`

Functions:

```python
global_threshold(
    image,
    threshold
)

adaptive_threshold(
    image,
    block_size,
    c_value,
    method
)
```

Optional:

```python
detect_contours(...)
```

We need at least two segmentation operations.

---

# 40. Global Thresholding

Function:

```python
global_threshold(image, threshold)
```

Control:

```text
Threshold:
0 ─────────●──────── 255

[Apply]
```

Flow:

```text
Image
 ↓
Grayscale
 ↓
cv2.threshold()
 ↓
Binary image
```

---

# 41. Adaptive Thresholding

Function:

```python
adaptive_threshold(
    image,
    block_size,
    c_value,
    method
)
```

Controls:

```text
Block Size:
[ 11 ]

Method:
[ Gaussian ▼ ]

C:
-20 ───────●────── +20

[Apply]
```

Methods:

```text
Mean
Gaussian
```

Validation:

```text
Block size must:
be integer
be greater than 1
be odd
```

---

# 42. Optional Contour Detection

Only implement after all required operations work correctly.

Function:

```python
detect_contours(
    image,
    threshold
)
```

Flow:

```text
Image
 ↓
Grayscale
 ↓
Threshold
 ↓
cv2.findContours()
 ↓
cv2.drawContours()
 ↓
Result
```

Contour detection is also listed as an available segmentation method in the assignment.

---

# 43. Dynamic Parameter Panel

Instead of building a separate screen for each operation, we will reuse one parameter panel.

Example:

Selecting Gaussian Blur shows:

```text
Gaussian Smoothing

Kernel Size:
[ 5 ]

Sigma:
────────●────────

[Apply]
```

Selecting Canny replaces those controls with:

```text
Canny Edge Detection

Threshold 1:
────────●────────

Threshold 2:
────────●────────

Aperture:
[3 ▼]

[Apply]
```

Implementation remains straightforward:

```python
def clear_controls():
    ...

def show_gaussian_controls():
    ...

def show_canny_controls():
    ...
```

---

# 44. Live Parameter Preview

Slider operations should update the preview interactively where practical.

Flow:

```text
Move slider
      ↓
Callback
      ↓
Process operation_source
      ↓
Display preview
```

Good candidates:

```text
Brightness
Contrast
Hue
Saturation
Value
Gaussian Sigma
Sobel Ratio
Canny T1
Canny T2
Global Threshold
Adaptive Threshold C
```

Textbox parameters can update after pressing **Apply**.

This keeps the implementation simple while satisfying the requirement for interactive parameter adjustment.

---

# 45. Apply Behavior

Operation flow:

```text
Select operation
      ↓
operation_source = current_image.copy()
      ↓
Adjust parameters
      ↓
Preview from operation_source
      ↓
Apply
      ↓
current_image = preview_result
```

This allows simple sequential processing.

Example:

```text
Original
 ↓
Brightness
 ↓ Apply
Brighter Image
 ↓
Gaussian Blur
 ↓ Apply
Blurred Brighter Image
 ↓
Canny
 ↓ Apply
Final Result
```

We do not need a sophisticated processing pipeline.

---

# 46. `utils/validators.py`

Functions can include:

```python
validate_integer()
validate_float()
validate_range()
validate_odd_kernel()
```

Example behavior:

```text
Valid:
3
5
7

Invalid:
-1
0
4
abc
```

The assignment says invalid parameters should not crash the application and defaults may be used when appropriate.

---

# 47. Error Handling

Use simple Tkinter dialogs:

```python
messagebox.showwarning(...)
messagebox.showerror(...)
messagebox.showinfo(...)
```

Examples:

```text
Please load an image before applying this operation.

Kernel size must be a positive odd number.

Please enter a valid numeric value.

Unable to access webcam.

There is no image to save.

Unable to open the selected image.
```

We do not need custom exception classes.

---

# 48. Edge Cases We Must Handle

```text
No image loaded

Invalid image file

No webcam available

Save attempted without image

Operation selected without image

Empty textbox

Non-numeric textbox

Negative kernel

Even kernel when odd is required

Invalid threshold

Invalid aperture

Close application while webcam is running
```

The application should show a useful message rather than crash.

---

# 49. Development Milestones

## Milestone 1 — Project Skeleton

Create:

```text
ComputerVisionApp/
├── main.py
├── app.py
├── gui/
├── core/
├── processing/
└── utils/
```

Goal:

```text
python main.py
```

opens the application successfully.

---

# 50. Milestone 2 — Basic GUI

Implement:

```text
Main Window
File Menu
Tools Menu
Image Preview Area
Parameter Panel
Apply Button
Reset Button
Snapshot Button
Status Bar
```

No processing yet.

---

# 51. Milestone 3 — Image I/O

Implement:

```text
Open JPG
Open JPEG
Open PNG
Open BMP
Display Image
Reset Image
Save Processed Image
```

Test completely before moving on.

---

# 52. Milestone 4 — Webcam

Implement:

```text
Start Webcam
Display Live Feed
Take Snapshot
Stop Webcam
Release Camera
```

At this stage all major input/output requirements are covered.

---

# 53. Milestone 5 — Color Operations

Implement:

```text
Grayscale
Brightness / Contrast
HSV Adjustment
```

Also establish the pattern for dynamic controls and live preview.

---

# 54. Milestone 6 — Statistics

Implement:

```text
Histogram
Histogram Equalization
```

These are mandatory.

---

# 55. Milestone 7 — Filters

Implement:

```text
Median Filter
Gaussian Smoothing
Sharpening
```

Add kernel validation.

---

# 56. Milestone 8 — Edge Detection

Implement:

```text
Sobel
Canny
```

Make sure required parameters are exposed instead of hardcoding them.

---

# 57. Milestone 9 — Segmentation

Implement:

```text
Global Threshold
Adaptive Threshold
```

At this point all required operation categories are complete.

---

# 58. Milestone 10 — Validation and Error Handling

Test:

```text
No image
Invalid image
No webcam
Invalid kernel
Negative kernel
Even kernel
Empty textbox
Text instead of number
Save without image
Exit during webcam
```

---

# 59. Milestone 11 — Optional Contours

Only implement if all mandatory functionality is stable.

---

# 60. Milestone 12 — UI Cleanup

Only simple improvements:

```text
Better spacing
Meaningful labels
Aligned buttons
Readable parameter controls
Window title
Status messages
Appropriate preview size
```

Do not spend time building sophisticated styling.

---

# 61. Milestone 13 — Full Testing

### File Handling

```text
□ JPG opens
□ JPEG opens
□ PNG opens
□ BMP opens
□ Image displays
□ Save works
□ Reset works
```

### Webcam

```text
□ Webcam opens
□ Live feed displays
□ Snapshot works
□ Webcam stops correctly
□ Webcam releases on exit
```

### Operations

```text
□ Grayscale
□ Brightness / Contrast
□ HSV Adjustment

□ Histogram
□ Histogram Equalization

□ Median Filter
□ Gaussian Smoothing
□ Sharpening

□ Sobel
□ Canny

□ Global Threshold
□ Adaptive Threshold
```

### Parameters

```text
□ Sliders work
□ Numeric text input works
□ Invalid numeric input handled
□ Kernel validation works
□ Range validation works
```

### Stability

```text
□ No-image operations don't crash
□ Save without image doesn't crash
□ Webcam failure doesn't crash
□ Window closes cleanly
```

---

# 62. Optional Bonus Features

The assignment mentions:

```text
Side-by-side original vs processed view
Preset buttons
Keyboard shortcuts
```

as possible bonus features.

We should not implement these until all mandatory features are complete.

If we add only one bonus, the best option is:

```text
Original                 Processed
┌─────────────┐          ┌─────────────┐
│             │          │             │
│    IMAGE    │          │    RESULT   │
│             │          │             │
└─────────────┘          └─────────────┘
```

This provides useful visual value without adding much complexity.

---

# 63. Documentation Plan

The assignment requires a **3–6 page PDF**.

Recommended structure:

## Page 1

```text
Title
Student Information
Video Link
Tool Overview
Main Features
```

## Page 2

```text
GUI Overview
Opening Images
Saving Images
Webcam
Snapshot
GUI Screenshot
```

## Page 3

```text
Foundations & Color
Statistics

Grayscale
Brightness / Contrast
HSV
Histogram
Histogram Equalization
```

## Page 4

```text
Filters
Edge Detection
Segmentation

Median
Gaussian
Sharpening
Sobel
Canny
Global Threshold
Adaptive Threshold
```

## Page 5

```text
Parameter Table
Screenshots
Conclusion
```

---

# 64. Parameter Table

Maintain this table while developing.

| Operation        | Parameter  | Input Type | Example Range     | Purpose               |
| ---------------- | ---------- | ---------- | ----------------- | --------------------- |
| Brightness       | Brightness | Slider     | -100 to 100       | Lighten/darken        |
| Contrast         | Contrast   | Slider     | 0.5 to 3          | Contrast strength     |
| HSV              | Hue        | Slider     | Defined range     | Hue adjustment        |
| HSV              | Saturation | Slider     | Defined range     | Color strength        |
| HSV              | Value      | Slider     | Defined range     | Brightness/value      |
| Median           | Kernel     | Textbox    | Odd 3–31          | Noise reduction       |
| Gaussian         | Kernel     | Textbox    | Odd 3–31          | Blur neighborhood     |
| Gaussian         | Sigma      | Slider     | 0–10              | Blur strength         |
| Sobel            | Kernel     | Menu       | 3/5/7             | Gradient neighborhood |
| Sobel            | Ratio      | Slider     | 0.1–3             | Edge threshold        |
| Canny            | T1         | Slider     | 0–255             | Lower threshold       |
| Canny            | T2         | Slider     | 0–255             | Upper threshold       |
| Canny            | Aperture   | Menu       | 3/5/7             | Sobel aperture        |
| Global Threshold | Threshold  | Slider     | 0–255             | Binary split          |
| Adaptive         | Block Size | Textbox    | Odd ≥3            | Local neighborhood    |
| Adaptive         | Method     | Menu       | Mean/Gaussian     | Threshold method      |
| Adaptive         | C          | Slider     | Approx. -20 to 20 | Threshold offset      |

Exact ranges can be finalized during implementation.

---

# 65. Demo Video Plan

The video must be **2–4 minutes** and include a link in the PDF.

Recommended flow:

### Start

```text
Launch application
```

### Open image

```text
File → Open Image
```

### Demonstrate at least four operations

Recommended:

```text
Brightness / Contrast
Gaussian Blur
Canny
Adaptive Threshold
```

Change parameters interactively.

### Webcam

```text
File → Access Live Webcam
```

Show live feed.

### Snapshot

```text
Take Snapshot
```

### Process snapshot

Apply one operation.

### Save

```text
File → Save As
```

Done.

There is no need to demonstrate all 12 operations in the video because the assignment explicitly asks for at least four.

---

# 66. Good Practices We Will Follow

```text
✓ Separate modules by responsibility

✓ Small and clear functions

✓ One clear application entry point

✓ Avoid global variables

✓ Keep state inside ComputerVisionApp

✓ Keep GUI logic separate from processing logic

✓ Processing functions receive images and return results

✓ Keep original and processed images separate

✓ Validate user input

✓ Reuse simple validation helpers

✓ Release webcam resources properly

✓ Show useful error messages

✓ Use meaningful names

✓ Add comments only for non-obvious logic

✓ Keep architecture understandable

✓ Avoid unnecessary complexity
```

---

# 67. Practices We Deliberately Avoid

```text
✗ Complex MVC architecture
✗ Service layer for every function
✗ Repository pattern
✗ Dependency injection
✗ Interfaces / abstract classes
✗ Factory patterns
✗ Plugin architecture
✗ Database
✗ REST API
✗ Authentication
✗ Docker
✗ Cloud integration
✗ Complex threading
✗ Production deployment system
✗ Undo/redo framework
✗ Image-history database
✗ Advanced UI design system
```

These would increase complexity without helping satisfy the assignment.

---

# 68. Final Detailed Folder Structure

```text
ComputerVisionApp/
│
├── main.py
│   └── Start Tkinter application
│
├── app.py
│   └── ComputerVisionApp
│       ├── application state
│       ├── select operation
│       ├── interactive preview
│       ├── apply result
│       ├── reset image
│       ├── take snapshot
│       ├── coordinate modules
│       └── clean application exit
│
├── gui/
│   │
│   ├── __init__.py
│   │
│   ├── layout.py
│   │   ├── create_menu()
│   │   ├── create_layout()
│   │   ├── create_image_area()
│   │   ├── create_control_area()
│   │   ├── create_status_bar()
│   │   ├── display_image()
│   │   └── update_status()
│   │
│   └── controls.py
│       ├── clear_controls()
│       ├── show_grayscale_controls()
│       ├── show_brightness_controls()
│       ├── show_hsv_controls()
│       ├── show_histogram_controls()
│       ├── show_median_controls()
│       ├── show_gaussian_controls()
│       ├── show_sobel_controls()
│       ├── show_canny_controls()
│       ├── show_global_threshold_controls()
│       └── show_adaptive_threshold_controls()
│
├── core/
│   │
│   ├── __init__.py
│   │
│   ├── file_handler.py
│   │   ├── open_image()
│   │   └── save_image()
│   │
│   └── webcam.py
│       ├── start_webcam()
│       ├── read_frame()
│       ├── stop_webcam()
│       └── is_webcam_available()
│
├── processing/
│   │
│   ├── __init__.py
│   │
│   ├── color.py
│   │   ├── grayscale()
│   │   ├── brightness_contrast()
│   │   └── adjust_hsv()
│   │
│   ├── statistics.py
│   │   ├── histogram()
│   │   └── histogram_equalization()
│   │
│   ├── filters.py
│   │   ├── median_filter()
│   │   ├── gaussian_blur()
│   │   └── sharpen()
│   │
│   ├── edges.py
│   │   ├── sobel()
│   │   └── canny()
│   │
│   └── segmentation.py
│       ├── global_threshold()
│       ├── adaptive_threshold()
│       └── detect_contours()     # Optional
│
├── utils/
│   │
│   ├── __init__.py
│   │
│   └── validators.py
│       ├── validate_integer()
│       ├── validate_float()
│       ├── validate_range()
│       └── validate_odd_kernel()
│
└── README.md
```

---

# 69. Final Definition of Done

The project is complete when:

```text
✓ Runs locally using python main.py

✓ Uses Python

✓ Uses OpenCV + Tkinter

✓ Opens JPG/JPEG

✓ Opens PNG

✓ Opens BMP

✓ Displays images

✓ Opens webcam

✓ Displays live webcam feed

✓ Takes webcam snapshot

✓ Switches snapshot to static-image mode

✓ Saves processed output

✓ Resets image

✓ Has File menu

✓ Has Tools menu

✓ Uses buttons

✓ Uses sliders

✓ Uses validated numeric textbox input

✓ Implements at least 10 operations

✓ Implements our planned 12 operations

✓ Meets all category minimums

✓ Histogram works

✓ Histogram Equalization works

✓ Median Filter works

✓ Gaussian Smoothing works

✓ Sobel required parameters work

✓ Canny required parameters work

✓ Global Threshold works

✓ Adaptive Threshold works

✓ Invalid input does not crash application

✓ No-image operation does not crash application

✓ Webcam resources release properly

✓ Code is separated into understandable modules

✓ Code is understandable enough to explain in interview

✓ PDF is 3–6 pages

✓ PDF contains overview

✓ PDF contains functionality descriptions

✓ PDF contains parameter table

✓ PDF contains screenshots

✓ PDF contains video link

✓ Demo video is 2–4 minutes

✓ Video shows at least four operations

✓ Video shows live parameter adjustment

✓ Video shows webcam

✓ Video shows snapshot

✓ Video shows saving output
```

---

# 70. Final Locked Scope

The final development direction is:

> Build a simple but well-structured Python desktop Computer Vision application using OpenCV and Tkinter. The project will use separate GUI, core, processing, and utility modules; one central `ComputerVisionApp` class; 12 primary computer-vision operations; dynamic operation controls; interactive preview where appropriate; image and webcam modes; snapshot support; validation; graceful error handling; proper webcam cleanup; and processed-image saving. More advanced architecture and bonus features will only be considered after every mandatory assignment requirement is complete.

This structure keeps the implementation clean and demonstrates good development practices without turning the assignment into unnecessarily sophisticated production software.
