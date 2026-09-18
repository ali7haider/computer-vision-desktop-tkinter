# app.py — Line-by-line study guide

Source: [app.py](../../app.py). This guide explains Python syntax, each variable's
purpose, and how the application connects its parts. The combined
[code documentation](../code-documentation.md) remains the project-wide guide.

Coverage: lines 1–80, through opening an image. Later methods are not
yet covered; extend this file as the study progresses. Line numbers refer to the
source read on 2026-09-18 and may shift after edits. These are code-reading notes,
not a record of new runtime tests.

## Lines 1–16: Description and imports

### Line 1

`"""Coordinate image state, file actions, preview, and application lifecycle."""`

This module docstring describes the file. The coordinator remembers images,
connects user actions to other modules, updates the preview, and handles closing.
Blank lines separate sections for readability; they do not perform actions.

### Line 3

`import tkinter as tk`

Imports Python's Tkinter GUI module under the shorter name `tk`. This alias lets
us write `tk.StringVar` and `tk.PhotoImage`. Importing it does not create a window.

### Line 4

`from tkinter import filedialog, messagebox`

Imports the file-dialog and message-dialog modules directly. `filedialog` asks
the user for file locations. `messagebox` displays errors and warnings.

### Line 6

`import cv2`

Imports OpenCV. This coordinator uses it to resize/convert previews and catch
`cv2.error`. Image-processing algorithms are implemented in `processing/`.

### Line 8

`from core.file_handler import load_image, save_image`

Imports functions that read and write image files. The imported `save_image`
function writes pixels; the app's `self.save_image` method coordinates the user
action, checks state, and opens the save dialog. These names are accessed
differently and refer to different functions.

### Line 9

`from core.webcam import Webcam`

Imports the camera-management class. Importing the class does not open a camera.
Its instances provide methods for starting, reading, and stopping capture.

### Line 10

`from gui.controls import OperationControls`

Imports the class that builds and manages the operation selector, parameters,
and action buttons. Keeping widget creation there separates GUI details from
application coordination.

### Line 11

`from gui.layout import create_layout, create_histogram_window, display_histogram`

`create_layout` builds the main layout and menus. `create_histogram_window`
creates the histogram window and returns its drawing canvas. `display_histogram`
draws already-calculated histogram counts. A canvas displays drawings and images.

### Line 12

`from processing.color import grayscale, brightness_contrast, rgb_channels`

Imports grayscale conversion, brightness/contrast adjustment, and independent
RGB-channel adjustment. Importing makes the functions available; it does not
apply an operation to an image.

### Line 13

`from processing.statistics import compute_histogram, equalize_histogram`

`compute_histogram` counts grayscale intensities. `equalize_histogram` performs
grayscale histogram equalization. Computing counts is separate from drawing them.

### Line 14

`from processing.filters import median_filter, gaussian_smoothing, sharpen`

Imports the median filter, Gaussian smoothing, and sharpening functions.

### Line 15

`from processing.edges import sobel_edges, canny_edges`

Imports the two implemented edge-detection functions.

### Line 16

`from processing.segmentation import global_threshold, adaptive_threshold, detect_contours`

Imports a single-threshold binary operation, local adaptive thresholding, and
contour detection/drawing.

## Lines 19–23: File-type options

```python
IMAGE_FILE_TYPES = [
    ("PNG image", "*.png"),
    ("JPEG image", "*.jpg *.jpeg"),
    ("BMP image", "*.bmp"),
]
```

- Line 19 creates a module-level list. Uppercase means it is intended as a
  constant; Python does not enforce that convention.
- Line 20 adds a tuple: the visible label and the PNG filename pattern.
- Line 21 adds the JPEG label and both supported JPEG filename patterns.
- Line 22 adds the BMP label and pattern.
- Line 23 closes the list. Trailing commas are valid Python syntax.

`*` matches filename text, so `*.png` matches names ending in `.png`. These
options are shared by the Open and Save dialogs to avoid repeating definitions.
Filtering filenames does not validate the actual image contents.

## Lines 26–28: Class, initialization, and the window

### Line 26

`class ComputerVisionApp:`

Defines a class grouping application state and actions. Calling
`ComputerVisionApp(root)` creates an instance of this class.

### Line 27

`def __init__(self, root):`

Defines the initializer called automatically for a new instance. `self` refers
to that instance; Python supplies it automatically. `root` is the existing
Tkinter main window passed by `main.py`. A function defined in a class is a method.

### Line 28

`self.root = root`

Stores a reference to the supplied window. The parameter `root` is local to this
method; the attribute `self.root` lets other methods use the same window later.
Assignment does not copy the window or create another one.

## Lines 29–43: Window settings and remembered state

### Line 29

`self.root.title("Interactive Computer Vision Tool")`

Sets the window title shown by the operating system.

### Line 30

`self.root.geometry("1000x650")`

Sets the initial width and height in pixels. The method expects a geometry string.

### Line 31

`self.root.minsize(700, 450)`

Sets minimum width and height so the controls remain usable when resizing.

### Line 32

`self.original_image = None`

Reserves an attribute for the original full-resolution pixel array from a file
or snapshot. `None` means no image has been assigned yet. Keeping original pixels
allows operations to start from the original and Reset to restore it.

Earlier discussion called this attribute `current_image`; the source now uses
`original_image` on this line. This guide follows the current spelling here.

### Line 33

`self.display_image = None # Result full-resolution pixel array.`

Stores the full-resolution result used for display and saving. It is separate
from the original so processing does not destroy the reset source. The comment
after `#` explains its purpose and is not executed.

### Line 34

`self.preview_photo = None # Tkinter-compatible image sized for the preview.`

Later holds a `tk.PhotoImage`, the representation Tkinter displays. Keeping a
Python reference prevents that image object from being garbage-collected and
disappearing from the canvas. The preview can be smaller than the saved result.

### Line 35

`self.resize_job = None`

Holds the identifier returned by `root.after` for a scheduled preview update.
It allows cancellation and prevents accumulating pending resize updates. `None`
means no update is pending. It is not a thread.

### Line 36

`self.processing_job = None`

Tracks a scheduled processing callback after slider changes. This is separate
from resizing: processing recalculates pixels; resizing redraws the preview.
Keeping its identifier also permits cancellation before reset or shutdown.

### Line 37

`self.histogram_canvas = None`

Later remembers the histogram drawing widget so the application can update and
reuse it. Initially no histogram has been created. A stored widget can later
be destroyed, which is why later methods also check `winfo_exists()`.

### Line 38

`self.webcam = Webcam()`

Creates and stores the camera manager. The object provides `start`, `read`, and
`stop` methods; constructing it does not begin live capture.

### Line 39

`self.webcam_running = False`

A Boolean recording whether the app is in live-camera mode. It determines which
image is previewed and guards processing/saving while the camera is active.

### Line 40

`self.webcam_job = None`

Tracks the scheduled next-frame callback so it can be cancelled when stopping
capture or exiting. This is independent of resize and processing callbacks.

### Line 41

`self.latest_frame = None`

Stores the latest camera frame as a pixel array. Live preview reads it; Snapshot
copies it. Keeping frames separate preserves the previous still-image result.

### Line 42

`self.static_status = None`

Temporarily saves the status text from before webcam mode. Stopping capture can
restore that text along with the previous still image. This stores text, not pixels.

### Line 43

`self.preview_status = tk.StringVar(self.root, value="No image loaded")`

Creates a Tkinter text variable associated with the main window's Tk environment.
`value` supplies the initial text. The layout connects a label's `textvariable`
to this object. Calling `.set("Applied: Grayscale")` updates that label;
`.get()` reads the text. Reassigning an ordinary Python string would not provide
this automatic widget connection.

## Lines 44–48: Build the layout and connect actions

```python
self.preview, controls_panel, self.snapshot_button, self.stop_button = create_layout(
    self.root, self.close, self.open_image, self.save_image,
    self.select_operation, self.reset_image, self.preview_status,
    self.start_webcam, self.take_snapshot, self.stop_webcam,
)
```

### Line 44

Calls `create_layout` and unpacks its four returned objects in order:

| Name | Returned object | Why remember it? |
| --- | --- | --- |
| `self.preview` | Preview canvas | Later methods draw images and read available dimensions. |
| `controls_panel` | Controls frame | Passed immediately to the controls constructor as its parent. |
| `self.snapshot_button` | Snapshot button | Webcam methods enable/disable it and access its containing frame. |
| `self.stop_button` | Stop button | Webcam methods enable/disable it. |

`controls_panel` is a local variable because no later app method needs to access
that frame by this name. The widgets retain their parent relationship after the
initializer returns. The three `self` attributes are needed by later methods.

The opening parenthesis allows the call to continue over multiple lines. Python
evaluates the right side before assigning the returned objects on the left.

### Line 45

Passes the main window and callbacks for Exit, Open, and Save. A callback is a
function given to another component to call when an event happens.

`self.close` passes a bound method, which remembers the application instance.
`self.close()` would run the method immediately. Here the methods must be passed
without parentheses so creating the interface does not trigger those actions.

### Line 46

Passes the operation-selection callback, Reset callback, and status text variable.
The Tools menu uses the callbacks. A label is connected to `preview_status`.
The status variable is data shared with a widget, not a callback.

### Line 47

Passes the callbacks for starting capture, taking a snapshot, and stopping capture.
The layout attaches them to the webcam menu item and camera buttons.

### Line 48

Closes the function call. All ten arguments are positional: their order matches
the parameters in `gui/layout.py`. The layout returns its canvas, controls frame,
snapshot button, and stop button in the order used on line 44.

## Lines 49–53: Create the operation controls

```python
self.controls = OperationControls(
    controls_panel, self.select_operation, self.apply_operation,
    self.reset_image, self.schedule_operation,
    self.save_image,
)
```

### Line 49

Constructs an `OperationControls` object and stores it on the app. Later methods
use it to read parameters, change operation selection, and enable/disable inputs.
This object manages controls; it is not the parent frame itself.

### Line 50

Passes the parent frame and callbacks for operation selection and Apply.
The selector forwards the chosen operation name to `self.select_operation`.
Clicking Apply calls `self.apply_operation`.

### Line 51

Passes Reset and parameter-change callbacks. Slider changes call
`self.schedule_operation`, which schedules processing rather than immediately
processing every slider event. Editable text parameters are applied with Apply.

### Line 52

Passes the Save callback for the panel's Save As button. The menu and button use
the same app method, avoiding two separate save workflows.

### Line 53

Closes construction. The GUI object is now available through `self.controls`.

## Lines 54–55: Register resize and close handlers

### Line 54

`self.preview.bind("<Configure>", self.schedule_preview)`

Registers a callback on the preview canvas. A Configure event happens when its
geometry changes, such as during resizing. Tkinter supplies an event object to
`schedule_preview(self, event)`. The method schedules a redraw, keeping the
preview fitted to the available space. Binding does not itself call the method.

### Line 55

`self.root.protocol("WM_DELETE_WINDOW", self.close)`

Registers the app's close method for the operating system's window-close request.
This lets the app cancel pending callbacks and release camera resources before
destroying the window. The File menu's Exit action uses this same method.

Initialization ends here. `main.py` then enters Tkinter's event loop, which
dispatches later clicks, window events, and scheduled callbacks.

## Lines 57–80: Open an image safely

### Line 57

`def open_image(self):`

Defines the method connected to File → Open. `self` gives it access to this app's
window, controls, images, and methods. There is no path parameter because the
method asks the user to select a file.

### Line 58

`path = filedialog.askopenfilename(`

Opens a file-selection dialog and stores the chosen filename/path in the local
variable `path`. For example, it might hold `/Users/student/Pictures/photo.png`.
This is a string locating the file, not image pixels. Cancelling normally returns
an empty string. This variable is only needed for the current Open action.

### Line 59

`parent=self.root,`

Associates the dialog with the main window. `parent` is a keyword argument to
the dialog function, not a new application attribute.

### Line 60

`title="Open Image",`

Supplies the dialog title. The operating system controls its exact presentation.

### Line 61

`filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]`

Begins the file-filter list with one combined option for supported image formats.
The tuple contains the visible label and filename patterns. This filters names;
it does not check the file's actual contents.

### Line 62

`+ IMAGE_FILE_TYPES + [("All files", "*")],`

Concatenates three lists: the combined image filter, individual PNG/JPEG/BMP
filters, and an All files option. The `+` operators create a combined list without
modifying `IMAGE_FILE_TYPES`. All files allows other filenames to be selected,
but `load_image` still rejects unsupported extensions and unreadable contents.

### Line 63

`)`

Closes the dialog call. Once the dialog returns, its result is assigned to `path`.

### Line 64

`if not path:`

Checks whether the result is empty. An empty string is false in a Boolean test,
so `not path` is true when no filename was chosen.

### Line 65

`return`

Exits this method on cancellation. It does not close the app. No image state is
replaced and the webcam is not stopped by this cancellation path.

### Line 66

`try:`

Starts a block for an operation that can fail for expected reasons, such as a
missing, unreadable, or corrupt file. Matching exceptions go to the `except` block.

### Line 67

`image = load_image(path)`

Calls the imported file-reading function. It validates the extension, reads bytes,
and decodes them into a BGR color NumPy array. The local variable `image` holds
those pixels, unlike `path`, which holds only the filename.

Keeping the result local until loading succeeds prevents a failed Open from
replacing the existing original image. This line does not display the new image.

### Line 68

`except (OSError, ValueError, cv2.error):`

Catches any of these expected exception types from the try block:

| Type | Example reason |
| --- | --- |
| `OSError` | Missing file or permission failure while reading. |
| `ValueError` | Unsupported extension, empty file, or undecodable image rejected by the loader. |
| `cv2.error` | An OpenCV decoding error. |

The tuple means any listed type is handled. Unrelated exceptions are not broadly
hidden. This handler covers the loading statement, not all subsequent method code.

### Line 69

`messagebox.showerror(`

Starts an error-dialog call, giving feedback about the unsuccessful Open action.

### Line 70

`"Open Failed",`

The first positional argument is the error-dialog title.

### Line 71

`"Could not open the image. Choose a valid, readable JPG, PNG, or BMP file.",`

The second positional argument is the user-facing explanation and recovery advice.

### Line 72

`parent=self.root,`

Associates the error dialog with the application's main window.

### Line 73

`)`

Closes the error-dialog call.

### Line 74

`return`

Stops this Open action after reporting the error. Without this return, execution
could reach code using `image` even though loading failed before assigning it.
The previous image or live-camera mode is preserved by this failure path.

### Line 75

`self.stop_webcam()`

Stops live capture and releases its resources before adopting the loaded image.
It can also be called when capture is inactive. Its placement after successful
loading ensures cancelled or failed Open actions do not stop live capture.

### Line 76

`# Preserve the loaded original separately from the result to display/save.`

A comment explaining the original/result separation. It performs no action.

### Line 77

`self.original_image = image`

Stores the successfully loaded pixel array as the app's original. This assignment
does not copy pixels; both names currently refer to the same array. The attribute
keeps the array accessible after the method's local variables go out of scope.
Reset below creates a separate copy for the displayed result.

### Line 78

`self.controls.set_image_loaded(True)`

Informs the controls manager that an image is available, allowing parameter
inputs to be enabled as appropriate. `True` is a Boolean, not an image itself.

### Line 79

`self.controls.choose("")`

Clears operation selection using an empty string. The controls manager removes
the previous operation's parameter widgets and shows the initial instruction.
A newly opened image therefore does not retain the previous operation selection.

### Line 80

`self.reset_image()`

Reuses the reset workflow: cancel pending processing, check image availability,
rebuild controls for the selection, copy the original into `display_image`, set
the original-image status, refresh the preview, and update an existing histogram.
Because line 79 cleared selection, Reset retains that empty selection here.

Successful flow: choose a file → load pixels → stop camera → store original →
enable controls → clear selection → display a separate copy of the original.
Cancellation and expected loading failures return before replacing image state.
