# Build Plan

## Project Goal

Build a simple, stable, and understandable desktop computer vision application using **Python, OpenCV, and Tkinter**.

The final application must:

* Open local images
* Access the webcam
* Take snapshots
* Apply at least 10 image-processing / computer-vision operations
* Provide interactive parameter controls
* Display processed results
* Save processed images
* Handle invalid actions without crashing
* Be easy to explain during academic evaluation

The priority is:

**Correctness → Stability → Simplicity → Usability → Visual Polish**

---

## Current Phase

**Phase: Planning / Project Setup**

No implementation should begin until the basic project structure, selected operations, and development plan are agreed.

---

# Milestones

```text
M1  Project Foundation
 ↓
M2  Image I/O + Basic GUI
 ↓
M3  Color + Statistics
 ↓
M4  Filters + Local Operators
 ↓
M5  Edge Detection
 ↓
M6  Segmentation
 ↓
M7  Webcam + Snapshot
 ↓
M8  Integration + Stability
 ↓
M9  Documentation + Demo
```

---

# Milestone 1 — Project Foundation

## Goal

Create the basic project structure and application shell.

## Scope

* Folder structure
* Python modules
* Tkinter root window
* Main application class
* Basic GUI layout
* Menu structure
* Image preview area
* Control area

## Dependencies

None.

## Tasks

* Create project folders.
* Create required Python files.
* Implement `main.py`.
* Create the main application class in `app.py`.
* Create basic GUI layout.
* Add File and Tools menus.
* Add empty image preview area.
* Add control panel area.
* Ensure application closes cleanly.

## Deliverables

A working application shell that launches using:

```bash
python main.py
```

## Verification

Verify:

* Application starts.
* Main window appears.
* Menu appears.
* Control area appears.
* Image preview area appears.
* Application closes normally.

## Completion Criteria

The application shell runs without errors and follows the agreed architecture.

---

# Milestone 2 — Image I/O + Basic GUI

## Goal

Allow the user to open, display, and save images.

## Scope

* File → Open...
* Image loading
* Image preview
* File → Save As...
* Basic image state

## Dependencies

Milestone 1.

## Tasks

Implement:

* Image file selection
* JPG support
* PNG support
* BMP support
* OpenCV image loading
* GUI image display
* Current/base image state
* Display/processed image state
* Save processed image

Handle:

* Cancelled Open dialog
* Invalid image
* Unsupported/unreadable file
* Save with no image
* Cancelled Save dialog
* Save failure

## Deliverables

The user can:

```text
Open Image
    ↓
View Image
    ↓
Save Image
```

## Verification

Test valid and invalid file actions.

No file-related user action should crash the application.

## Completion Criteria

Images can be opened, displayed, and saved reliably.

---

# Milestone 3 — Color + Statistics

## Goal

Implement the required foundational color and image-statistics functionality.

## Scope

Selected color operations:

1. **Grayscale Conversion**
2. **Brightness / Contrast Adjustment**
3. **RGB Channel Manipulation**

Required statistics operations:

4. **Histogram Computation and Display**
5. **Histogram Equalization**

This already satisfies the requirement to choose at least two operations from Foundations & Color, while implementing all required Image Statistics operations.

## Dependencies

Milestone 2.

## Tasks

Implement processing functions in:

```text
processing/color.py
processing/statistics.py
```

Add suitable GUI controls.

### Grayscale

Control:

```text
Menu / Button
```

### Brightness / Contrast

Controls:

```text
Brightness → Slider
Contrast   → Slider
```

Changes should update interactively.

### RGB Channels

Controls:

```text
Red   → Slider
Green → Slider
Blue  → Slider
```

### Histogram

Provide a way to calculate and display the histogram.

### Histogram Equalization

Provide a simple action to apply histogram equalization.

## Deliverables

Five working processing operations.

## Verification

For every operation test:

* Valid image
* No image loaded
* Minimum parameter
* Maximum parameter
* Normal parameter

## Completion Criteria

All five operations work correctly without causing crashes.

---

# Milestone 4 — Filters + Local Operators

## Goal

Implement required point/local image-processing operations.

## Scope

Implement:

6. **Median Filter**
7. **Gaussian Smoothing**
8. **Sharpening**

This provides more than the required minimum of two operations from this category.

## Dependencies

Milestone 3.

## Tasks

Implement functions in:

```text
processing/filters.py
```

### Median Filter

Parameters:

```text
Kernel Size → Textbox
```

Validate:

* Integer
* Positive
* Odd

### Gaussian Smoothing

Parameters:

```text
Kernel Size → Textbox / Slider
Sigma       → Slider / Textbox
```

Validate kernel and sigma before calling OpenCV.

### Sharpening

Use a simple sharpening implementation using a suitable kernel or Laplacian-based approach.

Keep the implementation easy to explain.

## Deliverables

Three working filter/local operations.

Running total:

```text
8 operations
```

## Verification

Test:

* Valid values
* Empty values
* Text instead of numbers
* Negative values
* Zero
* Invalid even kernel sizes
* Large values

## Completion Criteria

All operations work with valid input and invalid parameters are handled safely.

---

# Milestone 5 — Edge Detection

## Goal

Implement the required edge-detection operations.

## Scope

Implement:

9. **Sobel Edge Detection**
10. **Canny Edge Detection**

This satisfies the minimum requirement of two edge-detection methods.

## Dependencies

Milestone 4.

## Tasks

Implement functions in:

```text
processing/edges.py
```

### Sobel

Support the required parameters, including kernel size and threshold based on the required mean-ratio approach.

Validate kernel values before processing.

### Canny

Parameters should include:

```text
Threshold 1
Threshold 2
Aperture Size
```

Validate values before calling OpenCV.

## Deliverables

Two working edge-detection operations.

Running total:

```text
10 operations
```

## Verification

Test normal, minimum, maximum, and invalid parameter values.

Test each operation without an image loaded.

## Completion Criteria

Both edge-detection operations work reliably.

---

# Milestone 6 — Segmentation

## Goal

Satisfy the segmentation requirement.

## Scope

Implement:

11. **Global Thresholding**
12. **Adaptive Thresholding**
13. **Contour Detection**

This provides more than the minimum two segmentation operations.

## Dependencies

Milestone 5.

## Tasks

Implement functions in:

```text
processing/segmentation.py
```

### Global Thresholding

Provide threshold control.

### Adaptive Thresholding

Provide appropriate controls such as:

```text
Block Size
Method
Constant / C
```

Validate block size before processing.

### Contour Detection

Detect contours and display them on an image.

Keep the implementation straightforward.

## Deliverables

Three working segmentation operations.

Final planned operation count:

```text
13 operations
```

This is above the minimum requirement of 10.

## Verification

Test:

* Valid parameters
* Invalid parameters
* No image
* Different image types
* Boundary values

## Completion Criteria

All selected segmentation operations work without crashing.

---

# Milestone 7 — Webcam + Snapshot

## Goal

Add live webcam functionality.

## Scope

* File → Access Live Webcam
* Live webcam display
* Take Snapshot
* Stop webcam
* Snapshot becomes current image

## Dependencies

Milestone 2 and stable GUI.

## Tasks

Implement webcam functionality in:

```text
core/webcam.py
```

Add GUI integration.

Flow:

```text
Access Webcam
      ↓
Open Camera
      ↓
Display Frames
      ↓
Take Snapshot
      ↓
Stop Camera
      ↓
Snapshot becomes current image
      ↓
Process normally
```

Use Tkinter's event loop for webcam frame updates.

## Deliverables

Working webcam and snapshot functionality.

## Verification

Test:

* Webcam available
* Webcam unavailable
* Start webcam
* Stop webcam
* Take snapshot
* Process snapshot
* Exit while webcam is active
* Reopen webcam where supported

## Completion Criteria

Webcam works reliably and camera resources are always released safely.

---

# Milestone 8 — Integration + Stability

## Goal

Combine and verify the complete application.

This milestone is especially important because the application should not crash during evaluation.

## Scope

* Integration testing
* Validation
* Error handling
* GUI consistency
* Resource cleanup
* Final usability improvements

## Dependencies

Milestones 1–7.

## Tasks

Test complete workflows.

### Image Workflow

```text
Open
 ↓
Process
 ↓
Adjust Parameters
 ↓
Change Operation
 ↓
Save
```

### Webcam Workflow

```text
Webcam
 ↓
Snapshot
 ↓
Process
 ↓
Save
```

### Invalid Usage

Test:

* Operation without image
* Invalid numeric input
* Negative parameters
* Invalid kernel sizes
* Cancelled dialogs
* Invalid image
* Webcam unavailable
* Webcam read failure
* Save without image
* Repeated operations
* Closing application during webcam use

Fix any discovered crash paths.

## Deliverables

Stable integrated application.

## Verification

Perform a complete manual test of every feature and operation.

The application should either:

```text
Complete the operation
```

or:

```text
Show useful feedback and continue running
```

It should not terminate because of normal invalid user interaction.

## Completion Criteria

All required functionality works together and known expected error cases are handled safely.

---

# Milestone 9 — Documentation + Demo

## Goal

Prepare the project for final academic submission.

## Scope

* PDF documentation
* Screenshots
* Parameter table
* Demo video
* Final source review

## Dependencies

Milestone 8.

## Tasks

Create the required **3–6 page PDF**.

Include:

* Tool overview
* Implemented functionalities
* Operation descriptions
* Parameter table
* Parameter ranges
* Parameter effects
* GUI screenshots
* Demo video link

Record the **2–4 minute demonstration** showing:

* Opening an image
* At least four operations
* Live parameter adjustment
* Webcam access
* Taking a snapshot
* Saving output

Perform one final application test before recording.

## Deliverables

* Final Python application
* PDF documentation
* Demo video link
* Required submission package

## Verification

Confirm that every assignment requirement is represented in either the application or documentation as required.

## Completion Criteria

Application and submission materials are ready for evaluation.

---

# Future Work

Only consider additional features after all required functionality is stable.

Possible optional improvements:

* Side-by-side original vs processed view
* Preset buttons
* Keyboard shortcuts
* Additional processing operation

Bonus functionality must never be prioritized over required functionality or stability.

---

# Out of Scope

Do not add:

* Backend
* Database
* Authentication
* Cloud storage
* Web application
* PyQt
* Complex plugin systems
* Production monitoring
* Advanced architecture
* Unnecessary dependencies

---

# Known Dependencies

Required:

```text
Python
OpenCV
NumPy
Tkinter
```

Additional dependencies should only be introduced when clearly necessary.

---

# Known Risks

## Application Crashes

**Highest priority risk.**

Mitigation:

* Validate input before processing.
* Check image state.
* Check webcam state.
* Handle expected exceptions.
* Test invalid inputs.

## Invalid OpenCV Parameters

Operations may fail when given invalid kernel sizes, thresholds, or other parameters.

Mitigation:

```text
Input
 ↓
Validation
 ↓
OpenCV
```

Never send unchecked textbox values directly to OpenCV.

## Webcam Availability

The evaluator's camera may be unavailable or permission may be denied.

The application must handle this safely and remain running.

## GUI Freezing

Long/blocking operations can make Tkinter unresponsive.

Keep processing straightforward and use Tkinter's event loop for webcam updates.

## Overengineering

AI-generated code may introduce unnecessary architecture.

Mitigation:

Follow:

* `project-overview.md`
* `architecture.md`
* `code-standards.md`

Prefer the simplest implementation that satisfies the requirement.

---

# Build Rule

Complete and verify each milestone before moving to the next.

```text
Implement
   ↓
Run
   ↓
Test Normal Case
   ↓
Test Invalid Cases
   ↓
Fix
   ↓
Verify No Crash
   ↓
Mark Complete
   ↓
Next Milestone
```

A feature is **not complete simply because the code exists**.

It is complete when it works, handles expected invalid usage safely, and can be explained.
