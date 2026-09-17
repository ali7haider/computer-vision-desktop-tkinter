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

To run the source code on a new computer, start with
[Installation and Running](#15-installation-and-running-on-a-new-computer).
To create or use a packaged application, follow the section below.

## Build a Windows EXE or macOS App

[computer_vision.spec](computer_vision.spec) is the build recipe. PyInstaller bundles
Python, Tkinter, OpenCV, NumPy, and the application into a runnable package.
Only the person **building** needs Python and the build dependencies. The person
**using** the finished package does not need Python or pip.

Build the Windows `.exe` on Windows and the macOS `.app` on macOS. PyInstaller does
not create a Windows executable from a Mac. See the official
[platform build instructions](https://pyinstaller.org/en/stable/usage.html).
The original `python main.py` workflow remains available for the assignment.

### Windows: create the EXE

1. Install 64-bit Python 3.13 from [python.org](https://www.python.org/downloads/windows/),
   including Tcl/Tk support and the Python launcher.
2. Download/extract the complete project. Open PowerShell in the project folder
   containing `main.py` and `computer_vision.spec`.
3. Run these commands one at a time. Continue only if the previous command succeeds:

```powershell
py -3.13 -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-build.txt
.\.venv-build\Scripts\python.exe -m tkinter
.\.venv-build\Scripts\python.exe -m PyInstaller --noconfirm computer_vision.spec
```

The Tkinter command opens a small test window; close it before building.
No environment activation is needed. Internet access is required to download the
build dependencies. The first build can take several minutes.

After a successful build, the file to share is:

```text
dist\ComputerVisionTool.exe
```

This is a **portable application**, not a setup wizard. To install/use it on another
compatible Windows computer, copy the EXE into a folder you want to keep, then
double-click it. You can create a desktop shortcut to that file. If sent in a ZIP,
extract it first. To uninstall, close the app and delete the EXE and shortcut;
images you saved remain where you saved them.

The single EXE extracts its bundled libraries to a temporary folder when launched,
so startup can take a moment. This build is not publisher-signed. If Windows shows
a security warning, verify where the file came from; do not disable antivirus.
Build and test with the same Windows architecture as the intended recipient.

### macOS: create the app

Use a Python installation with working Tkinter, such as the Python 3.13 installer
from [python.org](https://www.python.org/downloads/macos/). In Terminal, change to
the project folder and run:

```bash
python3.13 -m venv .venv-build
.venv-build/bin/python -m pip install --only-binary=:all: -r requirements-build.txt
.venv-build/bin/python -m tkinter
.venv-build/bin/python -m PyInstaller --noconfirm computer_vision.spec
```

Close the Tkinter test window before building. If using this project's existing,
working `.venv`, the first command can instead be
`.venv/bin/python -m venv .venv-build`.

The finished application is:

```text
dist/ComputerVisionTool.app
```

Drag it into **Applications**, then double-click it. The `.app` contains its
dependencies; copying that complete app is sufficient. The additional
`dist/ComputerVisionTool` folder is an intermediate output, not needed when sharing
the `.app`. To uninstall, quit and move the app to Trash. Saved images remain.

Allow camera access when prompted if you want webcam snapshots. The build recipe
includes the camera permission description in the app's `Info.plist`, using
[PyInstaller's bundle configuration](https://pyinstaller.org/en/stable/spec-files.html#spec-file-options-for-a-macos-bundle).
Permission can be reviewed in System Settings → Privacy & Security → Camera.

The app is built for the architecture of the Python interpreter used (Apple Silicon
or Intel); it is not automatically a universal build. Test on the recipient's
macOS version and architecture. This recipe does not provide an Apple Developer ID
signature or notarization, so a downloaded copy may be blocked by Gatekeeper.
For a copy you built or trust, use the system's per-app approval flow if offered;
do not disable system security. For wider distribution, signing/notarization is
additional work.

### Rebuild and check before sharing

After changing source code, rerun the PyInstaller command for your OS. `--noconfirm`
replaces the previous generated output of the same name; keep any older release
you need elsewhere first. Generated `build/`, `dist/`, and `.venv-build/` folders
are excluded from Git. `requirements-build.txt` adds the packaging tool separately
from normal runtime dependencies.

Check the **packaged app**, including on a computer without Python if available:

1. Launch by double-clicking, open an image, apply operations, and view Histogram.
2. Try an invalid kernel size, correct it, and apply again.
3. Save a result and reopen it; cancel Open and Save dialogs.
4. Start the webcam, take a snapshot, process/save it, and start/stop again.
5. Close while the webcam is active and confirm the camera turns off.

A successful build alone does not prove GUI, camera, or another computer's
compatibility. Recorded packaging checks and remaining checks are in the
[progress tracker](context/planning/progress-tracker.md).

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

# 15. Installation and Running on a New Computer

These steps run the **source code**. If you already have the finished Windows
EXE or macOS app, use the [packaged-app instructions](#build-a-windows-exe-or-macos-app)
instead; those packages do not require a separate Python installation.

## Before you start

1. Install **64-bit Python 3.13 with Tkinter support**. This project's recorded
   local checks used Python 3.13; Windows still needs its own runtime verification.
2. Download and extract the complete project ZIP, or clone the repository.
   Keep `main.py`, `app.py`, `requirements.txt`, and the `gui`, `core`, `processing`,
   and `utils` folders together. Copying only `main.py` is not enough.
3. Open a terminal in the extracted project folder, where `main.py` and
   `requirements.txt` are located. Keep the path in quotes if it contains spaces.
4. Create a **new virtual environment on this computer** using the commands below.
   Internet access is needed to download dependencies during setup.

A virtual environment is a local folder containing a Python environment and this
project's installed libraries. **Do not copy `.venv` or `.venv-build` from another
computer or reuse a Mac environment on Windows.** They contain platform-specific
files and paths. Recreate the environment after moving the project to a different
location as well. This follows Python's
[virtual environment guidance](https://docs.python.org/3/library/venv.html#how-venvs-work).
Only recreate the environment folders; keep your source code and saved images.

`.venv` is for running/developing the source; `.venv-build` is for making the EXE/app.
Both are ignored by Git. `requirements.txt` tells pip which runtime libraries to
install on the new machine; `requirements-build.txt` also includes PyInstaller.

### Which command installs all the required libraries into `.venv`?

After creating `.venv`, run the command for your operating system from the project
folder. If you have not created it yet, follow the setup steps below first.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt
```

**macOS (Terminal):**

```bash
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
```

`-r requirements.txt` tells pip to install every library listed in that file
(OpenCV and NumPy), along with any dependencies they require. Using the Python
inside `.venv` installs those libraries into the **`.venv` folder**, rather than
your global Python installation. You do not need to install each library separately
or activate the environment first. `--only-binary=:all:` requests prebuilt packages.
Python and Tkinter must already be available as described in the setup steps.

## Windows setup (PowerShell)

Install Python 3.13 from [python.org](https://www.python.org/downloads/windows/)
with Tcl/Tk support and the Python launcher. Open a new PowerShell window afterward.
Replace the example folder below with your extracted project folder:

```powershell
cd "C:\path\to\computer-vision-desktop-tkinter"
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt
.\.venv\Scripts\python.exe -m tkinter
```

Run commands one at a time and resolve any error before continuing. The last
command should open a small Tkinter test window; close it, then launch:

```powershell
.\.venv\Scripts\python.exe main.py
```

These commands directly use the environment's Python. You do not need to activate
it or change PowerShell's script execution policy. If `py` is not found but
`python --version` reports Python 3.13, use `python` instead of `py -3.13` for the
version check and environment creation. Otherwise, check your Python installation.

## macOS setup (Terminal)

Install Python 3.13 with Tkinter from
[python.org](https://www.python.org/downloads/macos/). Use that installation rather
than assuming the system's `python3` includes a working Tkinter. Replace the
example folder below with your extracted project folder:

```bash
cd "/path/to/computer-vision-desktop-tkinter"
python3.13 --version
python3.13 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
.venv/bin/python -m tkinter
```

Run commands one at a time. Close the Tkinter test window, then launch:

```bash
.venv/bin/python main.py
```

File and Tools appear in the macOS system menu bar at the top of the screen when
the application is active. Camera access may require permission for the application
hosting Python.

## Running again later

Open a terminal in the project folder and run only your platform's launch command:

| Platform | Command |
| --- | --- |
| Windows PowerShell | `.\.venv\Scripts\python.exe main.py` |
| macOS Terminal | `.venv/bin/python main.py` |

You do not need to recreate the environment or reinstall dependencies each time.
If `requirements.txt` changes, rerun its installation command. A new computer or
moved environment needs fresh setup. In an IDE, select this project's local
`.venv` Python as the interpreter so its Run button uses the same dependencies.

## Common setup problems

| Problem | What to check |
| --- | --- |
| `python`, `py`, or `python3.13` is not found | Install Python for your OS, reopen the terminal, and check the version command. |
| `main.py` or `requirements.txt` is not found | Change to the extracted project folder before running the commands. |
| `No module named cv2` or `numpy` | Install requirements using the same `.venv` Python used to launch the app. |
| `No module named tkinter` or `_tkinter` | Repair/install a Python distribution with Tcl/Tk support, then recreate the environment with that Python. Tkinter is not installed by `pip install tkinter`. |
| A copied environment fails, or mentions another computer's path | Remove only the copied environment folder and create it again locally. |
| pip reports no matching binary distribution | Check that you are using 64-bit Python 3.13 and current pip. The chosen OS/architecture may not have compatible wheels; do not assume packages from another OS will work. |
| pip cannot reach the package server | Check your internet/proxy settings, then retry the installation command. |
| Webcam cannot open | Check camera permissions and availability, and whether another application is using it. Image-file processing can still be used. |

`--only-binary=:all:` requests prebuilt dependency packages, avoiding an accidental
OpenCV source compilation. If no compatible package is available, installation
stops with an error instead.

The Tkinter test is the standard check described in the
[Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html).
After setup, open an image, apply an operation, save the result, and test the
webcam if available. Use the detailed checks below for full verification.

## M2 Manual Verification

M2 is complete: automated checks passed and the user confirmed manual verification.
Keep this checklist for regression checks after future changes.

This checklist covers image opening, preview, and saving. M3 processing operations
are now available; see the M7 section for webcam controls.

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

## M5 Controls and Manual Verification

Sobel Edge Detection and Canny Edge Detection are available from Tools and the
Operation dropdown. Selection applies defaults. Edit parameters, then click
**Apply**; Reset restores the original and defaults while keeping the selection.
Both methods convert the original to grayscale and return a full-resolution
binary image: white edges on black. M5 brings the operation count to ten;
M6 adds the three segmentation operations described below; M7 adds webcam capture.

| Operation | Parameters | Behavior |
| --- | --- | --- |
| Sobel Edge Detection | Kernel dropdown: 3, 5, 7 (default 3); mean ratio textbox: 0–10 (default 1) | Computes horizontal/vertical derivatives and their magnitude. Pixels strictly above `ratio × mean magnitude` become white. |
| Canny Edge Detection | Threshold 1 textbox: 0–255 (default 100); threshold 2 textbox: 0–255 (default 200); aperture dropdown: 3, 5, 7 (default 3) | Uses a lower and upper gradient threshold to retain strong edges and connected weak edges. Threshold 1 must be ≤ threshold 2. |

Sobel thresholds the floating-point gradient magnitude before any clipping or
display conversion. Increasing its ratio retains fewer edges; zero retains all
nonzero gradients. Constant images remain black. The ratio range and Sobel kernel
selection are project choices for a manageable demonstration, not OpenCV limits.
Canny's 3/5/7 aperture selection follows its supported derivative sizes. Its
0–255 threshold range is a project choice, not a limit on gradient magnitudes;
larger apertures can change gradient strength substantially. No additional blur
is applied by the application. Both methods start from the original, so selecting
Gaussian Smoothing first does not create a processing chain.

1. Before loading an image, select both edge methods. Expect a warning and disabled
   parameter controls.
2. Open an image with clear boundaries. Try Sobel kernels 3, 5, and 7 and ratios
   0, 1, 2, and 10. Try an image with uniform color; it should remain black.
3. For Sobel ratio, try empty input, `abc`, `-1`, `11`, `nan`, and `inf`. Expect a
   warning with the previous result and applied-result label preserved.
4. Try Canny at 100/200, 0/255, and equal thresholds, with each aperture size.
   Try empty input, `abc`, `-1`, `256`, `nan`, and `inf` in each threshold field,
   then try threshold 1 greater than threshold 2. Expect clear warnings.
5. Correct invalid values and Apply again. Repeat Apply and verify the result does
   not accumulate changes. Edit parameters without Apply; the applied label stays.
6. Reset each method: the original returns, selection stays, and defaults return.
   Apply again. Keep Histogram open and check it updates with the edge result.
7. Save each result as PNG and reopen it to check full dimensions and appearance.
   Resize to the minimum window size, switch to earlier operations, open another
   image, and close normally.

## M6 Controls and Manual Verification

Three segmentation operations bring the total to thirteen. Select one from Tools
or the Operation dropdown to apply its defaults. Each starts from the loaded
original; operations do not accumulate. Reset restores the original/defaults and
retains the operation. Invalid input preserves the displayed result and its label.

| Operation | Controls | Result |
| --- | --- | --- |
| Global Thresholding | Live threshold slider 0–255, default 127 | Grayscale intensities strictly greater than the threshold become white; the rest become black. |
| Adaptive Thresholding | Odd block size 3–31, default 11; constant C −50–50, default 2; Mean/Gaussian dropdown, default Gaussian; Apply to process | Binary mask using each pixel's local mean or Gaussian-weighted neighborhood value minus C as its threshold. |
| Contour Detection | Live threshold slider 0–255, default 127 | Thresholds grayscale, then draws external boundaries of bright foreground regions in green, two pixels thick, on a copy of the original. |

Adaptive block size defines a square neighborhood. OpenCV requires an odd size
greater than one; the maximum of 31 is a project choice. C's −50–50 range is also a
project choice: increasing C lowers the local threshold and generally makes more
pixels white. Negative C raises it. OpenCV supports fractional C with integer-pixel
rounding, so very small changes may give the same mask. Border pixels are replicated
to extend neighborhoods, including when the block is larger than the image.

Contour Detection uses the same global threshold rule internally. Dark objects
on a bright background may instead yield an outline of the surrounding bright
region. Holes are not outlined, and no size filtering is applied. If there is no
foreground, the original is returned without outlines. Grayscale originals are
converted to BGR for the green overlay. Saving retains full dimensions; threshold
masks are grayscale and contour results are color images.

1. Before opening an image, select each new operation. Expect a warning and disabled
   parameter controls.
2. Open a detailed image. Move the Global Thresholding slider, including 0, 127,
   and 255. The display should update live; 255 should produce an all-black mask.
3. Try Adaptive Thresholding on uneven lighting. Apply both methods with blocks
   3, 11, and 31 and C values −50, 0, 2, and 50. The label should show the applied
   method and values. Edits alone should not change the result or its label.
4. For block size try empty input, `abc`, `0`, `-1`, `1`, `4`, `3.5`, and `33`.
   For C try empty input, `abc`, `-51`, `51`, `nan`, and `inf`. Expect clear warnings
   and the previous result to remain. Correct the values and Apply successfully.
5. Try Contour Detection on bright shapes against a dark background. Adjust the
   threshold and observe green outer boundaries. At 255 there should be no outlines.
6. Repeat Apply, Reset, and operation switching. Keep Histogram open and check that
   it updates. Try tiny and uniform images and the minimum window size.
7. Save/reopen each result as PNG; check dimensions and appearance. Open another
   image to clear the operation, then close after moving a live threshold slider.

## M7 Webcam Controls and Manual Verification

Choose **File → Access Live Webcam** to open the default camera (device 0).
Grant camera permission to the application hosting Python if the operating system
asks. On macOS, check **System Settings → Privacy & Security → Camera** if access
is denied. Another application using the camera may prevent access.

The **Save As…** button below Reset opens the same save dialog as File → Save As.
It saves the current full-resolution result and gives a warning when no image is
loaded or while the webcam is live.

The main preview shows the live feed. **Take Snapshot** and **Stop Webcam** are
below it and are visible only while capture is running. Both disappear after a
snapshot, Stop, capture failure, or opening an image.

* **Take Snapshot** copies the latest displayed frame at full resolution, releases
  the camera, and makes the snapshot the new original. Selection clears; choose
  any processing operation and save normally.
* **Stop Webcam** releases the camera and restores the previous image, result,
  parameters, and applied label. If no image was loaded, the empty preview returns.
* Processing controls are disabled during live capture. Tools, Apply, Reset, and
  Save As give a reminder to take a snapshot or stop first. Starting an already
  running webcam does not open another camera handle.
* Successfully opening an image stops capture and loads that image. Cancelling
  Open or choosing an unreadable file leaves capture running.
* An existing histogram closes when live capture begins. Reopen Histogram after
  a snapshot or Stop to view the static image's statistics.
* Capture failures stop and release the camera, restore the previous static
  preview, and show an error. Closing the application also releases the camera
  and cancels scheduled frame updates.

Frame reads use Tkinter's event loop, with the next read scheduled 30 ms after
processing the previous frame. This is not a guaranteed frame rate: camera/driver
latency and image size affect responsiveness. Opening or reading a camera can
briefly block while the driver responds. No video is recorded or saved automatically.

Automated checks use simulated cameras with real Tk windows. Physical camera
availability, permission prompts, image quality, and actual driver cleanup require
manual verification:

1. Launch the app, start the webcam, grant permission if prompted, and confirm a
   moving feed with correct colors and proportions. Resize the window, including
   its minimum size, and check that both webcam buttons remain visible.
2. Take Snapshot. Confirm the feed freezes and the camera indicator turns off.
   Try several operations, Reset, Histogram, and Save As; reopen the saved image.
3. Start again and use Stop Webcam. Confirm the prior static result returns and
   the camera turns off. Repeat start/stop and snapshot cycles.
4. Start without an image, then stop; the empty preview should return. Start with
   an image and edited parameters; Stop should retain that prior state.
5. During capture, try Tools, Apply, Reset, and Save As. Expect a reminder and an
   ongoing feed. Cancel Open, then open a valid image and confirm capture stops.
6. Test unavailable/denied camera access where possible. Expect an error and a
   usable application. If using an external camera, disconnect it during capture
   and check that failure restores the previous image. Reconnect and retry.
7. Close with capture active using both File → Exit and the window-close button.
   Confirm the camera indicator turns off and capture can be started after relaunch.



## M8 Integration and Stability Verification

All thirteen operations are integrated. Save As now preserves a copy of the
full-resolution result visible when the dialog opens. A pending live-slider
callback may update the preview while the native dialog is open, but it cannot
change the pixels selected for that save. Cancel still writes nothing.

Automated verification covers normal/invalid inputs, real Tk controls, simulated
camera failures and cleanup, and an end-to-end sweep of every operation on normal,
1×1, single-row, and single-column images. PNG/BMP saves are compared pixel for
pixel; JPEG is checked for output dimensions because it is lossy. Native dialog
interaction and actual camera hardware still require manual verification.

Use this final checklist alongside the parameter-specific M3–M7 checklists:

1. Launch with no image. Try processing, Reset, and both Save As entry points.
   Confirm clear warnings and that the app remains usable.
2. Open JPG, PNG, and BMP files. Run all thirteen operations, adjust parameters,
   repeat Apply, use Reset, and switch operations with Histogram open.
3. Try the invalid values listed in M4–M6. Confirm the displayed result and its
   label survive each error, then correct the input and apply successfully.
4. Save color, grayscale, binary, and contour results through both Save As entry
   points. Cancel Open/Save; try an unreadable image and invalid save destination.
   Confirm successful processing and saving still work afterward.
5. Move a live slider and immediately use Save As. The file should contain the
   result visible when Save As was invoked. Resize while working and check that
   controls fit at the minimum window size.
6. Start the physical webcam, take a snapshot, process it, and save it. Repeat
   start/stop; verify restored static state and hidden camera buttons after Stop.
7. Test camera unavailability where possible. Close during live capture and verify
   the camera indicator turns off. Relaunch and start capture again.
8. Close with a histogram open and immediately after moving a live slider. Check
   that the terminal has no Tk callback errors.

Known unresolved UI issue: the native macOS Save As sheet can initially appear
clipped before expanding. The reverted standalone-dialog workaround has not been
reintroduced. Record whether clipping remains in your manual run. M8 manual verification has been confirmed by the user. The clipping issue remains
recorded separately because its resolution was not explicitly confirmed. Automated
checks alone do not establish physical camera or native-dialog behavior.

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


## Editable M9 Report

[Computer Vision Project Report](Computer_Vision_Project_Report.docx) contains
all thirteen operations, parameter controls/ranges/effects, implementation notes,
and five screenshot placeholders with captions. Replace the student details and
placeholder content, then export to PDF from Word or a compatible editor.

The report is arranged into six planned pages. After inserting screenshots, check
page breaks, table layout, and the assignment's 3–6 page limit. No video is included
in this task; the assignment separately requires a 2–4 minute demo and its link on
the first PDF page. The native macOS Save dialog clipping issue remains recorded.

Project status: **M1–M9 complete for the agreed scope; ready for review.**
M9 delivers the editable DOCX and screenshot placeholders. Final screenshot
insertion/PDF export remain with the user; video was excluded from this task.
Further development will be planned after review feedback.
