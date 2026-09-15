# Architecture

## System Overview

The application is a standalone desktop computer vision tool built with:

* Python
* OpenCV
* Tkinter
* NumPy

The architecture separates the project into four main areas:

1. **GUI** — displays the interface and collects user input.
2. **Application** — coordinates GUI actions and application state.
3. **Core** — handles files and webcam access.
4. **Processing** — performs image-processing and computer-vision operations.

The architecture should remain simple and appropriate for an academic project.

---

## Architecture Diagram

```text
                    ┌─────────────────┐
                    │     main.py     │
                    │  Starts the App │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     app.py      │
                    │ Application     │
                    │ Coordinator     │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
       ┌───────────┐   ┌───────────┐   ┌──────────────┐
       │    GUI    │   │   Core    │   │  Processing  │
       │           │   │           │   │              │
       │ layout.py │   │ file      │   │ color        │
       │ controls  │   │ webcam    │   │ statistics   │
       └───────────┘   └───────────┘   │ filters      │
                                       │ edges        │
                                       │ segmentation│
                                       └──────────────┘
                                              │
                                              ▼
                                       Processed Image
                                              │
                                              ▼
                                           GUI
```

`app.py` acts as the central coordinator between these parts.

---

## Major Components

```text
ComputerVisionApp/
│
├── main.py
├── app.py
│
├── gui/
├── core/
├── processing/
└── utils/
```

### Entry Point

`main.py`

Starts the Tkinter application.

### Application Coordinator

`app.py`

Maintains application state and connects the GUI with core and processing functionality.

### GUI

`gui/`

Contains layout and interactive controls.

### Core

`core/`

Handles image files and webcam functionality.

### Processing

`processing/`

Contains computer-vision and image-processing algorithms.

### Utilities

`utils/`

Contains reusable validation helpers.

---

# Component Responsibilities

## `main.py`

Responsible only for starting the application.

Typical flow:

```text
Create Tkinter root
        ↓
Create application
        ↓
Start mainloop
```

Keep this file small.

---

## `app.py`

Acts as the central coordinator.

Responsible for:

* Current image
* Processed/display image
* Webcam state
* Connecting GUI actions to processing functions
* Updating the displayed result
* Coordinating application shutdown

Complex image-processing algorithms should not be implemented here.

---

## `gui/`

Responsible for the user interface.

### `layout.py`

Handles:

* Window layout
* Menu bar
* Image display area
* Placement of controls

### `controls.py`

Handles:

* Buttons
* Sliders
* Trackbars
* Textboxes
* Parameter controls

GUI modules collect user input but should delegate actual image processing to `processing/`.

---

## `core/`

### `file_handler.py`

Handles:

* Opening images
* Reading images
* Saving images
* File-related errors

### `webcam.py`

Handles:

* Opening webcam
* Reading frames
* Releasing webcam
* Webcam availability

The webcam must always be released safely when stopped or when the application exits.

---

## `processing/`

Processing modules contain simple functions that receive an image and parameters and return a processed result.

```text
processing/
├── color.py
├── statistics.py
├── filters.py
├── edges.py
└── segmentation.py
```

Example:

```python
def gaussian_blur(image, kernel_size, sigma):
    ...
    return processed_image
```

Processing functions should not directly control Tkinter widgets.

---

## `utils/validators.py`

Handles reusable validation such as:

* Numeric input
* Kernel sizes
* Odd-number requirements
* Parameter ranges

Its main purpose is to prevent invalid parameters from reaching OpenCV operations.

---

# System Boundaries

The application runs entirely on the user's local computer.

Inside the system:

* GUI
* Image processing
* Webcam handling
* File loading
* File saving

Outside the system:

* Operating system
* Local filesystem
* Webcam hardware

There is no backend, database, cloud service, or network API.

---

# Data Flow

## Image Processing Flow

```text
Open Image
    ↓
Load Image
    ↓
Store Current/Base Image
    ↓
User Selects Operation
    ↓
Read Parameters
    ↓
Validate Parameters
    ↓
Processing Function
    ↓
Processed Image
    ↓
Display in GUI
```

---

## Webcam Flow

```text
Access Live Webcam
        ↓
Open Camera
        ↓
Read Frames
        ↓
Display Frames
        ↓
Take Snapshot
        ↓
Copy Current Frame
        ↓
Stop + Release Camera
        ↓
Use Snapshot as Image
```

The snapshot can then go through the normal image-processing flow.

---

## Save Flow

```text
Displayed Image
      ↓
File → Save As...
      ↓
Select Destination
      ↓
Save Image
```

The **currently displayed processed result** should be saved.

---

# Interfaces / Contracts

Processing functions should generally follow:

```python
def operation(image, parameters):
    return processed_image
```

They should not modify unrelated application state.

The GUI communicates with processing functionality through `app.py`.

A simple dependency direction should be maintained:

```text
GUI
 ↓
APP
 ↓
CORE / PROCESSING
```

Avoid unnecessary circular dependencies.

---

# Data Storage

No database is required.

Application data exists in memory while the application is running.

Important state includes:

```text
base/current image
processed/display image
webcam state
latest webcam frame
current parameter values
```

Images are permanently stored only when the user chooses **Save As...**.

---

# Authentication

Not applicable.

The application has no accounts or login system.

---

# Authorization

Not applicable.

There are no user roles or permissions.

---

# External Integrations

The only external resources are:

* Local filesystem
* System webcam

No external APIs or cloud services are required.

---

# Background Processing

No separate background worker or service is required.

Webcam frames should use Tkinter's event loop, such as:

```python
root.after(...)
```

This keeps webcam updates integrated with the GUI without introducing unnecessary threading.

---

# Error Handling

Error handling is an important architectural requirement.

Expected problems must be handled without crashing the application.

Examples:

* No image loaded
* Invalid textbox input
* Invalid kernel size
* Invalid threshold
* Image cannot be opened
* Image cannot be saved
* Webcam unavailable
* Webcam frame cannot be read
* User cancels a dialog

General pattern:

```text
Validate
   ↓
Valid?
 ┌─┴─┐
No   Yes
│     │
▼     ▼
Message   Execute
│
▼
Return Safely
```

Expected user mistakes should result in a useful message or safe default, not application termination.

---

# Logging

No production logging system is required.

Simple console output may be used during development and debugging when useful.

User-facing problems should normally be shown through Tkinter messages.

---

# Observability

Not applicable.

Production monitoring, metrics, tracing, and alerting are outside the scope of this project.

---

# Security

Only basic local application safety is required.

The application should:

* Validate user input
* Avoid executing arbitrary user input
* Handle selected files safely
* Release webcam resources correctly

No production security infrastructure is required.

---

# Performance Considerations

Image operations should remain responsive for normal images used during demonstration.

Large images may be resized for GUI preview while preserving the actual image used for processing/saving where appropriate.

Webcam updates should avoid blocking Tkinter's main event loop.

No advanced performance optimization is required.

---

# Scalability Considerations

Not applicable.

This is a single-user local desktop application.

It does not need to support multiple users, servers, distributed processing, or large workloads.

---

# Deployment

There is no production deployment.

The application runs locally:

```bash
python main.py
```

Required Python dependencies must be installed before running the application.

---

# Environment Strategy

One local Python environment is sufficient.

Development and evaluation should use the same basic execution method:

```bash
python main.py
```

The application must not depend on Google Colab.

---

# Architecture Constraints

The following architecture rules should remain consistent:

1. Use Python.
2. Use OpenCV and Tkinter.
3. Keep the project modular but simple.
4. Do not introduce unnecessary folders or layers.
5. `main.py` remains the entry point.
6. `app.py` coordinates application state.
7. GUI code belongs in `gui/`.
8. File and webcam functionality belongs in `core/`.
9. Computer-vision algorithms belong in `processing/`.
10. Shared validation belongs in `utils/validators.py`.
11. Validate dangerous parameters before calling OpenCV.
12. Expected user mistakes must not crash the application.
13. Webcam resources must be released correctly.
14. Prefer simple code that can be explained during evaluation.

---

# Known Limitations

The application is intentionally limited to the assignment requirements.

Known limitations include:

* Local desktop use only
* One user at a time
* One webcam source
* No persistent application state
* No undo/redo system unless later required
* No cloud storage
* No remote processing
* No production monitoring
* No production deployment

These limitations are acceptable because they are outside the scope of the academic project.

---

# Architecture Principle

The architecture exists to make the code **easier to understand**, not to make the project more complex.

When deciding where code belongs:

```text
UI?                  → gui/
Application flow?    → app.py
Files / Webcam?      → core/
Image processing?    → processing/
Parameter validation?→ utils/
Startup?             → main.py
```

If a new abstraction, folder, or architectural layer does not clearly improve the assignment implementation, **do not add it**.
