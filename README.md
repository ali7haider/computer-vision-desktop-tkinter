# Interactive Computer Vision Tool with GUI

A desktop computer vision application built using **Python, OpenCV, and Tkinter**.

The application allows users to open images or use a webcam, apply different image-processing and computer-vision operations, adjust parameters interactively, preview the results, and save the processed output.

This project is developed as an **academic assignment**. The focus is on:

* Correct implementation
* Simple and understandable code
* Clear separation of responsibilities
* Interactive parameter control
* Input validation
* Safe error handling
* A GUI that remains stable during invalid operations

The project intentionally avoids unnecessary production-level complexity.

---

# 1. Technology

The project uses:

* **Python**
* **OpenCV**
* **Tkinter**
* **NumPy**

The application must run **locally from the terminal**.

Example:

```bash
python main.py
```

No web framework or PyQt is used.

---

# 2. Main Features

The application will provide a single desktop GUI for loading, processing, viewing, and saving images.

## Image Input

Users can:

* Open an image from their computer
* Support at least JPG, PNG, and BMP
* Access the system webcam
* View the webcam feed inside the application
* Take a snapshot from the webcam
* Continue processing the captured snapshot as a normal image

## Image Output

Users can:

* View the current processed result
* Save the currently displayed image using **File → Save As...**

## Interactive GUI

The interface includes:

* Menu bar
* Buttons
* Sliders / trackbars
* Numeric text inputs
* Image display area
* Webcam snapshot control
* Error/warning messages

Parameters should update the image interactively where appropriate.

---

# 3. Image Processing Operations

The application must implement at least **10 image-processing and computer-vision operations** while satisfying the required assignment categories.

Operations are organized by responsibility.

## Color and Foundations

Located in:

```text
processing/color.py
```

Examples include:

* RGB channel manipulation
* Grayscale conversion
* Brightness and contrast adjustment
* HSV adjustment
* Color blindness simulation

Only the operations selected for the final implementation need to be included.

## Image Statistics

Located in:

```text
processing/statistics.py
```

Required operations:

* Histogram computation and display
* Histogram equalization

## Filters and Local Operators

Located in:

```text
processing/filters.py
```

Possible operations include:

* Contrast stretching
* Median filtering
* Gaussian smoothing
* Sharpening

At least the required number of operations from this category will be implemented.

## Edge Detection

Located in:

```text
processing/edges.py
```

Possible operations include:

* Sobel edge detection
* Canny edge detection
* Laplacian of Gaussian (LoG)

At least the required number of edge-detection methods will be implemented.

## Segmentation

Located in:

```text
processing/segmentation.py
```

Possible operations include:

* Global thresholding
* Adaptive thresholding
* Contour detection

At least the required number of segmentation methods will be implemented.

---

# 4. Project Structure

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

The structure is intentionally kept small. Files are separated only where there is a clear responsibility.

---

# 5. File Responsibilities

## `main.py`

Application entry point.

Responsibilities:

* Create the Tkinter root window
* Create the application
* Start the Tkinter event loop

This file should remain very small.

---

## `app.py`

Main coordinator of the application.

Responsibilities:

* Main application class
* Maintain current application state
* Maintain the currently loaded image
* Maintain the currently displayed/processed image
* Connect GUI actions with processing functions
* Coordinate file handling
* Coordinate webcam operations
* Refresh the image preview
* Handle application shutdown safely

The main application logic belongs here.

---

# 6. GUI

## `gui/layout.py`

Responsible for the main GUI structure.

Examples:

* Main window layout
* Menu bar
* File menu
* Tools menu
* Image display area
* Control panel placement

It should focus on **where GUI elements appear**, rather than implementing image-processing algorithms.

## `gui/controls.py`

Responsible for interactive controls.

Examples:

* Buttons
* Sliders
* Trackbars
* Parameter text boxes
* Apply buttons
* Snapshot button

Processing algorithms should not be implemented directly inside GUI controls.

---

# 7. Core Functionality

## `core/file_handler.py`

Responsible for image file operations.

Examples:

* Open image
* Validate selected file
* Load image using OpenCV
* Save processed image
* Handle cancelled file dialogs
* Handle unsupported or unreadable files

## `core/webcam.py`

Responsible for webcam functionality.

Examples:

* Open webcam
* Check webcam availability
* Read frames
* Stop webcam
* Release camera resources
* Support snapshot capture

Camera resources must always be released correctly when they are no longer required.

---

# 8. Processing

The `processing/` package contains the actual computer-vision algorithms.

Processing functions should generally follow a simple pattern:

```python
def operation(image, parameter):
    # process image
    return processed_image
```

For example:

```python
def gaussian_blur(image, kernel_size, sigma):
    ...
    return result
```

Processing functions should remain:

* Small
* Readable
* Easy to test
* Easy to explain
* Independent from Tkinter where possible

A processing function should normally receive an image and parameters and return a result.

---

# 9. Validation

## `utils/validators.py`

Contains reusable validation for operation parameters.

Examples:

* Validate kernel size
* Ensure kernel size is odd
* Validate threshold range
* Validate numeric textbox input
* Validate positive values
* Apply safe defaults when appropriate

Validation should happen before potentially unsafe OpenCV operations are executed.

---

# 10. Critical Rule — The Application Must Not Crash

Application stability is an important requirement.

Expected user mistakes and common runtime problems must be handled safely.

For example:

### No Image Loaded

If the user selects an operation before opening an image:

```text
Please load an image before applying this operation.
```

The application should continue running.

### Invalid Numeric Input

If a textbox expects an integer but receives:

```text
abc
```

the application should display an understandable message or use an appropriate safe default.

It must not terminate because of a `ValueError`.

### Invalid Kernel Size

Operations such as Median or Gaussian filtering require valid kernel sizes.

Values such as:

```text
-1
0
4
abc
```

must be validated before calling OpenCV.

Depending on the operation, the application can:

* Inform the user about the valid value, or
* Replace an out-of-range value with an appropriate safe default

### Webcam Failure

If the webcam:

* Does not exist
* Cannot be opened
* Does not have permission
* Stops returning frames

the application should show an error message and remain usable.

### Invalid Image

If OpenCV cannot load the selected file, the application should inform the user instead of attempting to process an invalid image.

### Cancelled Dialogs

Cancelling:

* Open
* Save As

is a normal action and should simply return to the application.

---

# 11. Error-Handling Philosophy

Error handling should be **simple rather than overengineered**.

We do not need a complicated logging or exception framework.

The general flow should be:

```text
User Action
    ↓
Check required image/state
    ↓
Validate parameters
    ↓
Perform operation
    ↓
Display result
```

If something is invalid:

```text
Invalid Input
    ↓
Show useful message / apply safe default
    ↓
Return safely
    ↓
Application continues running
```

Expected user errors should never close the application.

---

# 12. Coding Guidelines

Because this is an academic project, readability is more important than clever abstractions.

Prefer:

```python
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

over unnecessarily complex class hierarchies or generic processing systems.

General rules:

* Keep functions focused
* Use meaningful names
* Add comments where the logic may not be obvious
* Avoid duplicated code where practical
* Validate parameters before OpenCV calls
* Keep processing separate from GUI code
* Release webcam resources correctly
* Avoid unnecessary dependencies
* Avoid unnecessary folders/classes/design patterns

Every part of the implementation should be understandable and explainable during the technical evaluation.

---

# 13. Development Approach

Development should happen incrementally.

A suitable sequence is:

```text
Basic application window
        ↓
Image opening/display
        ↓
Image saving
        ↓
Basic processing
        ↓
Interactive controls
        ↓
Required processing operations
        ↓
Webcam
        ↓
Snapshot
        ↓
Validation/error handling
        ↓
Integration testing
        ↓
Documentation
        ↓
Demo
```

Features should be tested as they are added instead of implementing everything first and testing only at the end.

---

# 14. Testing Priorities

Testing should focus heavily on preventing crashes.

Important cases include:

* Start application normally
* Close application normally
* Open valid JPG
* Open valid PNG
* Open valid BMP
* Cancel Open dialog
* Attempt to open invalid file
* Apply operation without image
* Apply each implemented operation
* Test minimum parameter values
* Test maximum parameter values
* Test invalid parameter values
* Test even/odd kernel constraints
* Test non-numeric textbox values
* Start webcam
* Take snapshot
* Stop webcam
* Handle unavailable webcam
* Save processed image
* Cancel Save As
* Exit while webcam is running

The expected outcome is always either:

```text
Successful operation
```

or:

```text
Useful user feedback + application continues running
```

Never an application crash.

---

# 15. Running the Application

Use a Python installation with Tkinter support, then create a virtual environment
and install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Tkinter is normally included with standard Python installations, but its availability depends on the operating system and Python installation.

Run the application from the project directory:

```bash
python main.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

On macOS, File and Tools appear in the system menu bar at the top of the screen
when the application is active.

## M2 Manual Verification

M2 is complete: automated checks passed and the user confirmed manual verification.
Keep this checklist for regression checks after future changes.

This checklist covers image opening, preview, and saving. M3 processing operations
are now available; webcam controls remain disabled until M7.

1. Launch the app and select **File → Save As...** before opening an image.
   Expect a warning, with the app staying open.
2. Select **File → Open...**, then cancel. The empty preview should remain.
3. Open a JPG, PNG, and BMP in turn. Each should appear with correct colors
   and proportions. Also try a filename containing spaces or accented characters.
4. Resize the window with a large image loaded. The preview should fit without
   stretching or cropping; the original image resolution is preserved.
5. Save using **File → Save As...** to new `.png`, `.jpg`, and `.bmp` files.
   Reopen them and check their appearance and full pixel dimensions. JPEG is
   lossy, so small pixel differences are expected.
6. Cancel Open and Save As with an image loaded. The displayed image should stay
   unchanged, and cancelling Save As should create no file.
7. Try opening a text file using **All files**, an empty `.png`, and a text file
   renamed to `.jpg`. Expect an error and the previous image to remain visible.
8. Try saving with an unsupported extension (such as `.xyz`) or to a folder
   without write permission. Either the native dialog rejects the destination
   or the app shows an error; the image should remain usable.
9. Open and save another valid image after an error. Repeat several times,
   then close via **File → Exit**. Relaunch and test the window close button.

## M3 Controls and Manual Verification

M3 is complete: automated checks passed and the user confirmed manual verification,
including Reset. Keep this checklist for future regression checks.

Select an operation in **Tools** or the **Operation** dropdown. Selection applies
the operation immediately; sliders update the result live. **Apply** repeats the
selected operation. Each image-changing operation starts from the loaded original,
so adjustments do not accumulate. **Reset** restores the original and resets slider
values to their defaults while keeping the selected operation. For operations
without parameters, it restores the original; Apply runs the selected operation
again. Reset does not ask for confirmation. Opening another image clears the selection.

| Operation | Controls / ranges | Expected result |
| --- | --- | --- |
| Grayscale | No parameters | Converts color pixels to grayscale intensities. |
| Brightness / Contrast | Brightness: −255 to 255 (default 0); contrast: 0 to 3 (default 1, step 0.05) | Computes `contrast × pixel + brightness`, rounded and clipped to 0–255. |
| RGB Channels | Red, green, blue gains: 0 to 2 (default 1, step 0.05) | Multiplies each channel independently; 0 removes it, 1 preserves it, 2 doubles it with clipping. |
| Histogram | No parameters | Opens a graph of the displayed image's 256 grayscale intensity counts; the image stays unchanged. |
| Histogram Equalization | No parameters | Converts the original to grayscale, then redistributes its intensities to improve contrast where possible. |

The histogram's horizontal axis is intensity (0–255), and its vertical axis is
pixel count. An open histogram updates when the displayed image changes. It is
drawn using Tkinter; no plotting dependency is required. Save As saves the image
result, not the histogram graph.

1. Before opening an image, try each Tools operation, Apply, and Reset. Expect a
   warning and a usable application. Parameter sliders should be disabled.
2. Open a colorful image. Choose Grayscale and save the result as PNG. Reopen the
   saved file to check its appearance and original pixel dimensions.
3. Reopen the color original. Choose Brightness / Contrast and drag each slider
   continuously. Try brightness −255, 0, and 255, and contrast 0, 1, and 3.
   With brightness 0, contrast 0 should produce black. With contrast 1, brightness
   −255 should produce black and 255 should produce white.
4. Return brightness to 0 and contrast to 1: the original should return exactly.
   Repeated Apply should not keep brightening the image.
5. Choose RGB Channels. Set each channel gain to 0 individually and observe its
   removal. Set all three to 0 for black, all to 1 for the original, and try 2
   to check clipping. The sliders limit input to the allowed range.
6. Open Histogram after an adjustment. Check that it describes the current
   result without changing it. Keep the graph open while adjusting another
   operation, then resize it, close it, and reopen it.
7. Choose Histogram Equalization on a low-contrast image. Expect a grayscale
   result with more spread-out intensities. A uniform image may stay unchanged.
   Compare its histogram with the original using Reset.
8. Switch repeatedly between operations and use Reset. Check that the selection
   stays, brightness returns to 0, contrast/RGB gains return to 1, and the original
   image appears without a confirmation prompt. Open another image with
   sliders or a histogram active; the new original should appear with cleared controls.
9. Try the controls at the minimum window size. Save both color and grayscale
   results, cancel dialogs, and repeat M2 invalid-file checks. Close the app with
   the histogram open and after moving a slider.

Algorithm references: OpenCV's [brightness/contrast tutorial](https://docs.opencv.org/4.x/d3/dc1/tutorial_basic_linear_transform.html)
and [histogram equalization tutorial](https://docs.opencv.org/4.x/d4/d1b/tutorial_histogram_equalization.html).

## M4 Controls and Manual Verification

M4 and the applied-result label are user-verified. Keep this checklist for future
regression checks. Range-selection rationale is in
[Code Documentation](context/code-documentation.md#19-why-these-parameter-ranges).

Three more operations are available in Tools and the Operation dropdown. Selecting
one applies its defaults. Edit textbox values and click **Apply** to run again;
typing alone does not process the image or interrupt you with warnings.

The label above the preview identifies the **applied operation and parameter
values**. Editing text does not change that label until Apply succeeds. Invalid
input leaves the prior result and label intact. Open/Reset show **Original image —
no operation applied**; viewing a histogram keeps the image's existing label.

| Operation | Parameters | Behavior |
| --- | --- | --- |
| Median Filter | Kernel size: odd integer 3–31, default 3 | Replaces each pixel with the neighborhood median; useful for isolated speckle noise. |
| Gaussian Smoothing | Kernel size: odd integer 3–31, default 5; sigma: 0–10, default 0 | Weighted local smoothing. Sigma 0 lets OpenCV derive sigma from the kernel size. |
| Sharpening | Fixed 3×3 kernel, no parameters | Emphasizes local differences using center weight 5 and four neighboring weights −1. |

The kernel limit keeps interactive processing practical. Larger kernels generally
smooth more; sigma controls Gaussian spread within the selected kernel. Sharpening
may also emphasize noise. All operations use the loaded original, preserve full
dimensions, and can be saved. Reset restores the original and default parameters
while retaining the selected operation, without a confirmation dialog.

1. Before loading an image, select each filter. Expect a warning and disabled textboxes.
2. Open a detailed/noisy image. Try Median Filter with kernels 3, 5, and 31.
3. Try Gaussian Smoothing with kernels 3, 5, and 31, and sigma 0, 1, and 10.
   Edit text and confirm the result changes only after Apply.
4. For both kernel fields try empty input, `abc`, `0`, `-1`, `1`, `4`, `3.5`, and
   `999`. Each should show a clear warning and preserve the previous result.
5. For sigma try empty input, `abc`, `-1`, `11`, `nan`, and `inf`. Expect warnings.
   Then enter valid values and confirm processing still works.
6. Try Sharpening and repeat Apply. The result should not become progressively
   sharper because each application starts from the original.
7. Change filter parameters, then Reset. Verify the operation stays selected,
   defaults return, and the original reappears. Apply should run the filter again.
8. Keep Histogram open while applying filters. Resize the main window, save/reopen
   a result, open another image, switch to M3 operations, and exit normally.

Webcam access, when implemented, will require the operating system to grant camera permission to Python/Terminal.

---

# 16. Academic Requirements

For a code-level walkthrough of verified milestones, see
[Code Documentation](context/code-documentation.md).

This is an individual academic assignment.

AI tools may be used to assist development and debugging, but the final code must be understood by the student.

The student should be able to explain:

* Project structure
* GUI event handling
* Image representation
* OpenCV operations
* Parameters
* Validation
* Webcam lifecycle
* How each implemented computer-vision operation works
* Why particular parameter ranges were selected

Code should therefore remain straightforward and defensible.

---

# 17. Submission

The assignment documentation is an important part of the final submission.

## PDF Documentation

The PDF should be approximately **3–6 pages** and include:

* Overview of the tool
* List of implemented functionalities
* A subsection for each implemented operation
* Parameter table
* Valid parameter ranges
* Explanation of parameter effects
* GUI screenshots
* Demo video link

## Python Script

The application source code must launch the GUI and support:

* Image mode
* Webcam mode
* Interactive processing
* Output saving

## Demo Video

The demonstration should be approximately **2–4 minutes**.

It should demonstrate:

* Opening an image
* At least four processing operations
* Live parameter adjustment
* Webcam access
* Taking a snapshot
* Saving the processed result

The video link should be included near the beginning of the PDF.

---

# 18. Project Goal

The goal is not to create a commercial image-editing application.

The goal is to demonstrate understanding of:

* OpenCV
* Image-processing concepts
* Computer-vision operations
* Tkinter GUI programming
* Interactive parameter control
* Input validation
* Webcam handling
* Safe application behavior

The final application should therefore be:

**Simple, structured, stable, understandable, and complete enough to satisfy the assignment requirements.**
