# Code Documentation

This guide explains how the verified application works, so the student can trace
the code and explain it during evaluation. It covers **M1–M5**:

* M1 foundation: commit `3b953a0`.
* M2 image loading, preview, and saving: commit `b0c57a2`.
* M3 color and statistics: commit `ccfd624`.
* M4 filters and applied-result label: user-verified on 2026-09-16.
* M5 Sobel and Canny edge detection: user-verified on 2026-09-16.

The explanations below describe the verified implementation through M5. Update
this guide after user verification, before committing future implementation changes.

For installation and manual checks, see [README](../README.md). For verification
results and milestone status, see the [progress tracker](planning/progress-tracker.md).

## 1. Code Map

| File | Responsibility |
| --- | --- |
| `main.py` | Create the Tkinter root, create the application, start the event loop. |
| `app.py` | Own image state and connect file actions, preview updates, and shutdown. |
| `gui/layout.py` | Create menus, arrange panels, and return the preview canvas. |
| `gui/controls.py` | Manage the operation selector, sliders, textboxes, parameter dropdowns, Apply, and Reset. |
| `processing/color.py` | Grayscale, brightness/contrast, and RGB channel manipulation. |
| `processing/statistics.py` | Compute intensity histograms and equalize grayscale images. |
| `processing/filters.py` | Median filtering, Gaussian smoothing, and sharpening. |
| `processing/edges.py` | Sobel mean-ratio thresholding and Canny binary edge maps. |
| `utils/validators.py` | Validate finite numbers, ranges, odd filter kernels, and edge kernel/aperture choices. |
| `core/file_handler.py` | Validate file extensions, decode images, and encode/save images. |
| Package `__init__.py` files | Mark `gui`, `core`, `processing`, and `utils` as regular Python packages. |
| `requirements.txt` | Declare OpenCV 4.x and NumPy 2.x dependency ranges. |
| `.gitignore` | Exclude Python cache files and the local `.venv` environment from Git. |

M3 adds color/statistics functions and numeric validation to the previously empty
packages. M4 adds local filters and textbox validation. M5 adds edge detection
and parameter dropdowns. Segmentation and webcam belong to later milestones.

The package markers contain descriptions, not initialization logic. They make
imports such as `from gui.layout import create_layout` explicit and conventional.
Python executes a package's `__init__.py` when first importing that package.

## 2. Startup: `main.py`

```text
python main.py
    → main()
    → tk.Tk()
    → ComputerVisionApp(root)
    → root.mainloop()
```

`tk.Tk()` creates the main window and its Tcl/Tk interpreter. The interpreter is
the underlying system that implements Tkinter's widgets and events.

`ComputerVisionApp(root)` configures that window and connects its actions.
`root.mainloop()` then waits for events such as menu selections, window resizing,
and closing. Tkinter invokes the corresponding Python functions when events occur.

The guard `if __name__ == "__main__":` starts the application only when this file
is run directly. Importing `main` does not open a window automatically.

### Why pass functions instead of calling them?

In `app.py`, layout creation receives `self.close`, `self.open_image`, and
`self.save_image`, plus `self.select_operation` and `self.reset_image`. These are
**callbacks**: functions to call later.

For example, `command=on_open` connects a menu item to the open action. Writing
`command=on_open()` would run it immediately while constructing the menu.

## 3. Application State: `ComputerVisionApp`

The constructor sets the title, initial size (`1000×650`), and minimum size
(`700×450`). It initializes the following attributes:

| Attribute | Initial value | Meaning |
| --- | --- | --- |
| `root` | Tkinter root | Main window and event-loop access. |
| `current_image` | `None` | Full-resolution image loaded from the file. |
| `display_image` | `None` | Full-resolution result used for preview and saving. |
| `preview_photo` | `None` | Tkinter-compatible image used by the canvas. |
| `resize_job` | `None` | Identifier of a scheduled preview update, if one exists. |
| `preview` | Canvas returned by layout | Widget on which the preview is drawn. |
| `processing_job` | `None` | Identifier of a scheduled slider-driven operation. |
| `histogram_canvas` | `None` | Canvas in the optional histogram window. |
| `controls` | `OperationControls` instance | Owns selector and parameter widgets/variables. |
| `preview_status` | `StringVar` saying “No image loaded” | Describes the actual displayed result, independently of selected/edited controls. |

The constructor also binds canvas `<Configure>` events to `schedule_preview` and
the window-close protocol `WM_DELETE_WINDOW` to `close`.

### Original, result, and preview are different things

After loading, `open_image` stores the original and calls `reset_image`, which
creates the independent result. The relevant assignments are:

```python
self.current_image = image
self.display_image = self.current_image.copy()
```

`.copy()` gives the result its own pixel storage. Assigning `display_image = image`
would make both names refer to the same array; later edits through one reference
could change the other. Loading and Reset give both arrays identical content but
separate storage; processing then replaces only `display_image`.

The preview is a smaller, temporary representation of `display_image`. It never
replaces the full-resolution result. Saving therefore does not reduce resolution
just because the application window is small.

### What is an image in memory?

`load_image` returns a NumPy array with shape `(height, width, 3)` and type `uint8`.
Each channel value is between 0 and 255. OpenCV stores color channels as **BGR**:
blue, green, red. For example, `[0, 0, 255]` is a red pixel.

Loading uses `cv2.IMREAD_COLOR`, which normalizes input to a three-channel color
image. A grayscale file is loaded with three channels; PNG transparency is not
preserved. M2 saves pixel content, not original file metadata.

## 4. GUI Construction

### `gui/layout.py`: `create_layout(root, on_exit, on_open, on_save, on_select, on_reset, preview_status)`

This function creates the File and Tools menus and attaches the menu bar with
`root.configure(menu=menu_bar)`.

At the end of M4:

* Open, Save As, Exit, all eight operations, and Reset have callbacks.
* Webcam remains disabled.

The Tools menu loops through `OPERATIONS`. Its callback uses `lambda name=operation`
to capture each current operation name, so every menu item invokes its own operation.

On macOS, the active application's menus appear in the system menu bar at the top
of the screen. They do not appear as a row inside the application window.

The function uses `grid` to arrange the controls on the left and preview on the
right. `sticky="nsew"` lets a widget fill its grid cell in all directions.
Row/column `weight=1` allows a cell to receive extra space when its parent grows.
The preview column gets the extra horizontal space; the controls keep their
requested width.

The preview canvas starts with requested dimensions of `1×1`, allowing the grid
to determine its actual size. It has a white background. The function returns
`(canvas, controls)` so `app.py` can draw previews and construct `OperationControls`
in the control panel. File-handling logic remains outside the layout module.

### `gui/controls.py`: `OperationControls`

This class replaces M1/M2's placeholder `create_controls` function. A class keeps
related widget references and parameter values together without adding another
application coordinator. It does not process images.

* `operation` is a `StringVar` connected to a read-only combobox.
* `choose(operation)` rebuilds only the relevant parameter controls with defaults.
* `add_slider(...)` creates a labeled `Scale` backed by a `DoubleVar`.
* `values` maps parameter names to those variables; `sliders` stores widget references.
* `add_entry(...)` creates a labeled textbox backed by a `StringVar`.
* `entries` stores textbox widgets, alongside `sliders`.
* `set_image_loaded(loaded)` enables/disables sliders and entries.
* `get_parameters()` returns numeric keyword arguments for processing functions.

Dropdown selection invokes the coordinator's selection callback. Slider movement
invokes its scheduling callback. Apply and Reset call coordinator methods directly.

## 5. Opening an Image

```text
File → Open...
    → ComputerVisionApp.open_image()
    → askopenfilename()
    → core.file_handler.load_image(path)
    → store original and independent result
    → refresh_preview()
```

### `ComputerVisionApp.open_image()`

The native file dialog uses filters from `IMAGE_FILE_TYPES`, a combined image
filter, and an All Files option. Filters help selection; they do not validate
the actual contents of a file.

If the user cancels, the dialog returns an empty path and the method returns
immediately. Otherwise, it calls `load_image(path)` inside a `try` block.
Application image state changes only after loading succeeds. This is why opening
a corrupt file leaves the previous image visible.

### `validate_extension(path)`

`Path(path).suffix.lower()` extracts a case-insensitive extension. The supported
set is `.jpg`, `.jpeg`, `.png`, and `.bmp`. The function returns the extension or
raises `ValueError` if it is unsupported. Both loading and saving use this check.

### `load_image(path)`

1. Validate the extension.
2. Read encoded file bytes with `np.fromfile(path, dtype=np.uint8)`.
3. Reject an empty file before attempting to decode it.
4. Decode with `cv2.imdecode(data, cv2.IMREAD_COLOR)`.
5. Reject `None`, which means OpenCV could not decode an image.
6. Return the pixel array.

NumPy handles the filesystem path, while OpenCV decodes the bytes. This supports
filenames containing Unicode characters without relying on OpenCV's path handling.

**Example:** renaming a text file to `photo.jpg` passes extension validation, but
decoding fails. The GUI displays “Open Failed” and keeps the existing image.

## 6. Rendering the Preview

`refresh_preview()` first cancels any pending resize job and clears its identifier.
This also handles an immediate refresh after opening a file, when a resize update
might already be scheduled.

It reads the canvas dimensions, enforcing a minimum of one pixel, and removes
the previous canvas items. With no image loaded, it draws “Open an image to begin.”

With an image loaded, it follows these steps:

### Fit the image without stretching

```python
scale = min(width / image_width, height / image_height, 1.0)
```

Both image dimensions use the same scale, preserving proportions. The `1.0`
cap prevents enlarging an image beyond its original pixel dimensions. Integer
rounding can produce a small, approximately one-pixel difference in proportions.

For an image of `1600×900` and a canvas of `800×600`:

```text
scale = min(800/1600, 600/900, 1) = 0.5
preview = 800×450
saved image = 1600×900
```

The unused vertical space becomes padding. `cv2.resize` uses `INTER_AREA`, which
is suitable for shrinking the preview. Each computed dimension is at least one
pixel, including for very thin images.

### Convert OpenCV pixels for Tkinter

The code converts BGR to RGB with `cv2.cvtColor`. It also supports a two-dimensional
grayscale result by converting it to three RGB channels for display.

It then constructs binary **PPM** data: a short header describing the dimensions
and channel maximum (`255`), followed by raw RGB bytes. Tkinter's `PhotoImage`
can read this format directly, so Pillow is not needed.

The resulting `PhotoImage` is stored in `self.preview_photo`. Keeping this Python
reference prevents garbage collection from removing the image while the canvas
still uses it. `create_image(width / 2, height / 2, ...)` centers the preview.

## 7. Updating During Window Resizing

Canvas size changes generate `<Configure>` events. Each calls
`schedule_preview(event)`:

```python
if self.resize_job is None:
    self.resize_job = self.root.after(40, self.refresh_preview)
```

`after` schedules work in Tkinter's event loop; it does not create a thread or
sleep inside the event handler. There is only one pending update. Additional
resize events leave that update in place rather than postponing it.

```text
Resize event → schedule update
More resize events → keep the pending update
About 40 ms later → refresh using the latest canvas dimensions
Next resize event → schedule another update
```

This is called throttling: limiting how often work runs while still updating
during a continuous stream of events. The earlier delay-until-resizing-stops
behavior was replaced during M2. The 40 ms delay is a scheduling target, not a
guaranteed frame rate; Tkinter can run it later if the event loop is busy.

## 8. Saving an Image

```text
File → Save As...
    → ComputerVisionApp.save_image()
    → check display_image exists
    → asksaveasfilename()
    → core.file_handler.save_image(path, display_image)
    → encode bytes → write destination
```

The application method and file helper share the name `save_image` but have
different responsibilities. `self.save_image()` manages the GUI action;
`save_image(path, image)` is the imported file helper.

The GUI warns before opening the save dialog if there is no image. The default
extension is `.png`; the user can select PNG, JPEG, or BMP. Cancelling simply
returns without writing anything.

The helper validates the extension and calls `cv2.imencode(extension, image)`.
It checks the success flag, then writes the encoded bytes with `encoded.tofile(path)`.
The extension determines the output format. Saving uses `display_image`, never
the canvas pixels or `preview_photo`.

Encoding happens before opening the destination. An encoding failure therefore
does not erase an existing file. This is not an atomic save: a filesystem failure
during writing can still leave a partial file. Expected write errors are reported
by the GUI.

PNG/BMP round trips preserve tested pixel values; JPEG compression can change
them slightly. All three formats retain the full image dimensions.

## 9. Expected Error Handling

File helpers report problems by raising exceptions; they do not create dialogs.
`app.py` catches the expected exception types and shows short messages.

| Situation | Detection | GUI behavior |
| --- | --- | --- |
| Open/Save cancelled | Empty dialog path | Return without changing state or writing. |
| Save without image | `display_image is None` | Show “No Image”; do not open save dialog. |
| Unsupported extension | `validate_extension` raises `ValueError` | Show Open/Save Failed. |
| Empty/corrupt image | Empty byte array or failed decode | Show Open Failed; preserve previous image. |
| Missing/unreadable file | `OSError` from file access | Show Open Failed; preserve previous image. |
| Invalid/unwritable save path | `OSError` from writing | Show Save Failed; keep in-memory image. |
| OpenCV decoding/encoding error | `cv2.error` | Show Open/Save Failed and return. |

The handlers catch `(OSError, ValueError, cv2.error)`, not every exception. This
handles anticipated file problems without silently hiding unrelated coding bugs.
The normal event loop continues after the callback returns.

## 10. Shutdown

Both File → Exit and the window close button invoke `ComputerVisionApp.close()`.
It calls `cancel_processing()`, cancels a pending preview update, clears the job
identifiers, and calls `root.destroy()`.

Cancelling first prevents delayed code from trying to redraw destroyed widgets.
Destroying the root closes the main window and any histogram child window, then
lets `mainloop()` return. No camera is opened through M4, so there are no webcam
resources to release yet.

## 11. Walkthrough to Explain During Evaluation

Suppose the user opens `holiday.png`, resizes the window, then saves `result.bmp`:

1. The File menu invokes `open_image`; a dialog returns the source path.
2. The file helper checks `.png`, reads bytes, and decodes BGR pixels.
3. The coordinator stores the original and a separate full-resolution result.
4. Preview rendering calculates a fitted size, converts BGR to RGB, builds a
   PPM image, and draws it on the canvas.
5. Resizing schedules periodic redraws using the latest canvas dimensions.
   Neither full-resolution array changes.
6. Save As returns a `.bmp` path. The helper encodes `display_image` as BMP and
   writes it at the original dimensions.
7. Closing cancels any pending redraw and destroys the window.

If the user attempts to open an invalid file between steps 5 and 6, loading fails
before image state is replaced. They can still save the previously loaded image.

## 12. M3 Operation Flow

```text
Tools menu / Operation dropdown
    → select_operation(name)
    → cancel pending processing
    → controls.choose(name): rebuild controls with defaults
    → apply_operation()
    → require_image()
    → read parameters → validate → processing function
    → display_image = result
    → refresh_preview() → update_histogram() if open
```

`require_image()` warns and returns `False` when no original is loaded. Apply
also warns when no operation is selected. Slider widgets are disabled without an
image, while menus and buttons remain available to provide this feedback.

`apply_operation()` dispatches through explicit `if/elif` branches. Each
image-changing function receives `current_image`, not the previous result. The
Histogram branch instead reads `display_image` and returns without replacing it.
This means only one adjustment is active; operations are not a cumulative pipeline.

**Example:** Grayscale produces a two-dimensional result. Selecting Brightness /
Contrast afterward uses the original color image, so color returns. Repeated
Apply at unchanged settings produces the same output, rather than compounding it.

### Live sliders and Apply

`schedule_operation()` schedules one `after(40, self.apply_operation)` callback.
Further slider events keep that callback in place; it reads the latest values
when it runs. This uses the same scheduling idea as preview resizing, with a
separate `processing_job` identifier. All processing runs on Tkinter's event loop.

`cancel_processing()` cancels and clears that job. Selection changes, Apply,
Reset, and shutdown call it to avoid applying stale work later. Apply explicitly
recomputes the selected operation; with live sliders it often produces no visible
change because the latest result is already shown.

### Reset versus opening a new image

`reset_image()` cancels pending processing, checks for an image, and calls
`controls.choose(self.controls.operation.get())`. Rebuilding the controls restores
their defaults while retaining the selected operation. It then copies the
original to `display_image`, refreshes the preview, and updates any open histogram.

* Brightness resets to 0; contrast and each RGB gain reset to 1.
* Grayscale and equalization stay selected, but the original image is restored.
  Apply runs the selected operation again.
* Histogram stays selected and its graph updates to describe the original.
* There is no confirmation dialog; Reset never overwrites the source file.

A successful `open_image()` first enables controls and calls `controls.choose("")`,
then calls Reset. This deliberately clears the selection for a new source image.
Cancelled or failed opens leave the existing image and settings intact.

## 13. Color Algorithms: `processing/color.py`

All functions return a new array and leave the input unchanged. They accept the
application's uint8 BGR images; grayscale inputs are also supported.

### `grayscale(image)`

For a two-dimensional image, return a copy. Otherwise, use
`cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)` to combine channels into a weighted
intensity, approximately `0.114 × B + 0.587 × G + 0.299 × R`.

For example, a pure red BGR pixel `[0, 0, 255]` becomes intensity 76. The result
has shape `(height, width)`. Preview rendering converts it to RGB for Tkinter,
while saving uses the actual grayscale array.

### `brightness_contrast(image, brightness=0, contrast=1)`

Validate brightness in `[-255, 255]` and contrast in `[0, 3]`. Compute:

```text
result = contrast × original pixel + brightness
```

Convert to `float32` before arithmetic so uint8 values cannot wrap around.
`np.rint` rounds the values; `np.clip(..., 0, 255)` limits them; `astype(np.uint8)`
returns normal image pixels. Negative results become zero, not their absolute value.

**Example:** pixel 100 with contrast 1.5 and brightness −20 becomes 130. Pixel 10
with brightness −50 and contrast 1 becomes 0. Defaults reproduce the original.
Contrast 0 with brightness 0 produces black.

### `rgb_channels(image, red=1, green=1, blue=1)`

Validate each gain in `[0, 2]`. Convert a grayscale input to BGR if necessary.
Build a gain array in OpenCV order: `[blue, green, red]`. NumPy broadcasts these
three multipliers across every pixel, then rounds, clips, and converts to uint8.

For a BGR pixel `[50, 100, 200]`, red gain 0 with other gains 1 produces
`[50, 100, 0]`. All gains 1 preserve the original; all gains 0 produce black.
The GUI uses increments of 0.05 for channel gains and contrast, and 1 for brightness.

## 14. Statistics: `processing/statistics.py`

### `compute_histogram(image)`

Convert to grayscale, then call:

```python
cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
```

Channel `[0]` selects the grayscale channel; `None` means no mask, so every pixel
counts. There are 256 bins over `[0, 256)`, including intensity 255. `.ravel()`
turns the returned column array into a one-dimensional array of counts.

For `[0, 0, 128, 255]`, bins 0, 128, and 255 contain 2, 1, and 1; all others
contain zero. Counts total the number of pixels for the tested images. The
histogram is of grayscale intensity, not three separate RGB distributions.

### `equalize_histogram(image)`

Convert to grayscale and call `cv2.equalizeHist`. Equalization uses the cumulative
intensity distribution to map populated levels across a wider range. The output
is grayscale; it does not preserve color.

For `[100, 100, 110, 120]`, the result is `[0, 0, 128, 255]`. Uniform images stay
uniform, so this operation does not always visibly change an image or guarantee
a perfectly flat histogram. It always operates on the loaded original in this GUI.

## 15. Histogram Window and Lifecycle

`show_histogram()` creates a window if `histogram_canvas` is absent or its widget
has been destroyed. Otherwise it reuses the existing window. It updates the graph
and raises the window with `lift()`.

`create_histogram_window(root)` creates a child `Toplevel` containing an expanding
canvas. `update_histogram()` computes counts from `display_image` and passes them
to `display_histogram(canvas, counts)`. It does nothing if the window is closed.

The drawing function scales 256 bars to the plot's width and the highest count to
its height, then labels intensity and pixel-count axes. Its resize callback
redraws from the supplied counts; no image-processing algorithm lives in the GUI.
The graph updates after processing, Reset, or successfully opening another image.

The canvas stores `histogram_resize_callback`, the binding identifier returned by
Tkinter. Before replacing the resize handler, the old binding and its Tcl command
are removed with `unbind`. This prevents handlers from accumulating as sliders
update the graph. Closing the child window destroys its widgets; opening Histogram
again creates a fresh canvas. Closing the main app destroys the child as well.

Save As continues to save `display_image`, not a screenshot of the graph.

## 16. Numeric Validation and Processing Errors

`validate_number(value, name, minimum, maximum)` converts input with `float`,
rejects conversion failures, checks `math.isfinite`, and enforces inclusive bounds.
It returns the validated number or raises a clear `ValueError`.

Sliders constrain ordinary input, but validation inside processing functions also
protects direct calls from invalid values such as `"abc"`, `NaN`, or infinity.
Negative brightness is valid; negative contrast or RGB gain is not.

The coordinator handles:

* `tk.TclError` while reading an invalid Tk numeric variable: parameter warning.
* `ValueError` from validation or an empty operation selection: specific warning.
* `cv2.error` from processing: a short processing-failed message.

The result is assigned to `display_image` only after the selected image operation
succeeds. These errors therefore preserve the prior result. Programming errors
outside the expected cases are not hidden by a catch-all exception handler.

## 17. M4 Filter Controls and Execution Flow

M4 adds Median Filter, Gaussian Smoothing, and Sharpening to `OPERATIONS`. The
existing menu and dropdown automatically include these names. `apply_operation()`
has a branch for each new function in `processing/filters.py`.

```text
Select filter → build default controls → apply defaults
Edit textbox → retain text without processing
Click Apply → read strings → validate → filter original → replace result
    → set applied-result label → refresh preview and any open histogram
```

`OperationControls.add_entry(label, name, default)` creates a `ttk.Entry` backed
by a `StringVar` and stores it in `values` under the function parameter name.
For example, `kernel_size` maps directly to the processing function's argument.
`get_parameters()` returns strings for textboxes and numbers for sliders.

Using `StringVar` allows incomplete or invalid text to exist while the user is
editing. Validation happens on Apply, so deleting a value temporarily does not
trigger a warning. Textbox edits have no live-processing callback. Selection
still applies the default filter immediately, consistent with other operations.

Reset rebuilds the selected operation's controls with defaults and restores the
original pixels. It does not reapply the filter until Apply is pressed. Gaussian
Reset restores kernel `5` and sigma `0`; Median Reset restores kernel `3`.

## 18. Filter Algorithms: `processing/filters.py`

### `median_filter(image, kernel_size=3)`

Validate the kernel, then call `cv2.medianBlur(image, kernel)`. Each output channel
value is the median of its local square neighborhood. This can remove isolated
bright/dark noise while retaining edges better than averaging in many cases.

For example, a 3×3 neighborhood with eight zeros and one 255 has median zero.
A constant image remains constant. OpenCV handles image boundaries internally;
the output retains the input dimensions and uint8 type.

### `gaussian_smoothing(image, kernel_size=5, sigma=0)`

Validate the kernel and sigma, then call:

```python
cv2.GaussianBlur(image, (kernel, kernel), sigmaX=sigma)
```

This computes a weighted local average, with larger weights near the center.
The square kernel sets the neighborhood size; sigma controls how broadly the
weights spread within it. The omitted vertical sigma follows the horizontal
sigma. Sigma zero asks OpenCV to derive the spread from the kernel size.

For example, smoothing a single bright pixel on a black background lowers its
peak and spreads brightness into neighboring pixels. A constant image stays
constant. Increasing sigma with a fixed small kernel has limited effect because
the neighborhood still contains the same small number of pixels.

### `sharpen(image)`

The fixed kernel is:

```text
 0  -1   0
-1   5  -1
 0  -1   0
```

`cv2.filter2D(image, -1, kernel)` applies it independently to image channels.
The `-1` preserves the input depth; results outside uint8 range saturate to 0 or
255. The center is amplified and its four immediate neighbors are subtracted.
The weights sum to one, so constant areas remain unchanged.

**Example:** a center value of 120 surrounded by four values of 100 becomes
`5 × 120 − 4 × 100 = 200`. A neighboring 100 next to that center becomes 80,
emphasizing their difference. Sharpening can also amplify noise and cause halos.
There is no adjustable strength parameter in M4.

All three functions return a new image. The application passes the loaded
original to them, so repeated Apply does not compound filtering.

## 19. Why These Parameter Ranges?

The assignment requires valid, documented parameters and safe invalid-input
handling. It does **not** specify the exact upper limits used here.

| Parameter/rule | Reason and whether it is a requirement or a project choice |
| --- | --- |
| Odd kernel dimensions | Required by the selected OpenCV median/Gaussian calls with explicit square kernels; odd sizes have a center pixel and symmetric neighbors. |
| Minimum kernel 3 | Project choice: 3×3 is the smallest useful smoothing neighborhood. A 1×1 neighborhood would leave the image unchanged. |
| Maximum kernel 31 | Project choice: bounds the neighborhood and processing work, especially for median filtering, while allowing a broad demonstration range. It is not an OpenCV maximum. |
| Median default 3 | Starts with mild filtering and a small neighborhood, making its effect easy to compare with the original. |
| Gaussian default 5 | Provides a modest, visible smoothing neighborhood without beginning at an extreme blur. |
| Sigma 0 | Supported automatic mode: OpenCV derives sigma from kernel size. It is also the default so users can start by changing only the kernel. |
| Positive sigma up to 10 | Project choice: gives a useful finite adjustment range alongside kernels up to 31. Ten is not an OpenCV maximum and is not universally optimal for every image. |
| Reject negative/nonfinite sigma | The UI exposes automatic zero or positive spread only. Negative values have no useful standard-deviation meaning in this interface; NaN and infinity are rejected before OpenCV. |

The upper bounds are practical starting policies, **not benchmark-derived
performance thresholds** or guarantees that every image size will process quickly.
A kernel of 31 uses a 31×31 neighborhood, compared with 3×3 for the minimum.
Larger neighborhoods generally require more work, but exact cost depends on the
algorithm and image dimensions. These limits can be revised if a real use case
requires it; validation, labels, documentation, and boundary checks must then agree.

### Kernel validation details

`validate_kernel_size(value)` strips surrounding whitespace and accepts ASCII
decimal digits only. It rejects more than two digits before integer conversion,
then enforces 3–31 and odd parity. This avoids sending decimal fractions, negative
values, even values, or enormous strings to OpenCV.

The current text format intentionally rejects `3.0`, `+3`, and `003`; users should
enter a simple integer such as `3`. `03` is accepted. All invalid cases use the
same clear message: “Kernel size must be an odd integer from 3 to 31.”
Sigma uses `validate_number`, which accepts numeric text and checks finite values
and the inclusive range 0–10. On failure, the coordinator warns and retains the
previous result. Correcting the input and pressing Apply works normally afterward.

## 20. Applied-Result Label

The selected operation and edited parameters are not necessarily the operation
and values that produced the visible image. `preview_status` explicitly records
what is currently displayed.

`create_layout` receives this `StringVar` and connects it to a label above the
preview canvas. The label occupies row 0; the expanding canvas occupies row 1.
The text wraps so it remains readable in a narrow window.

| Event | Label behavior |
| --- | --- |
| Launch | `No image loaded` |
| Successful Open or Reset | `Original image — no operation applied` |
| Successful processing | `Applied: <operation>` plus the actual applied parameter values |
| Textbox edit without Apply | Retain the previous applied label |
| Invalid input or failed processing | Retain the previous applied label and pixels |
| Live slider update | Update the label when the new result is produced |
| Histogram selection | Keep the image's label, since the histogram does not change its pixels |

After a successful image-changing operation, `apply_operation()` builds the label
from the operation name and the captured parameters. Underscores become spaces,
parameter names use title case, and numeric values use compact `:g` formatting.
The label changes only after validation and processing succeed.

**Example:** Median Filter is applied with kernel 3, then the user types 5. The
label still says `Kernel Size: 3` until Apply succeeds. Typing `abc` and pressing
Apply shows a warning while the kernel-3 result and label remain. Reset retains
Median Filter in the selector, but correctly labels the displayed pixels as the
original image rather than claiming that a filter is still applied.

## 21. M5 Controls and Execution Flow

M5 adds `Sobel Edge Detection` and `Canny Edge Detection` to `OPERATIONS`, so both
appear in the existing Tools menu and operation selector. The application now has
ten operations. Each new branch in `apply_operation()` calls its function in
`processing/edges.py` with `current_image` and the selected parameters.

```text
Select edge method → rebuild controls → apply defaults
Edit textbox or parameter dropdown → wait for Apply
Apply → check image → read parameters → validate → compute binary edge map
    → replace displayed result → update applied label, preview, and histogram
```

`OperationControls.add_choice(label, name, options, default)` creates a
`ttk.Combobox` backed by a `StringVar`. It stores that variable in `values` under
the processing function's parameter name and records the widget in `choices`.
The dropdown uses `readonly` when an image is loaded and `disabled` otherwise.
`choose()` clears the old widget lists when rebuilding controls;
`set_image_loaded()` updates dropdown state alongside entries and sliders.

The edge parameter dropdowns have no processing callback. Like M4 textboxes,
their edits take effect on Apply. This differs from the live M3 sliders.
`get_parameters()` returns strings for both edge textboxes and dropdowns.

Reset retains the operation, restores its default controls, and shows a copy of
the original. It does not immediately run edge detection again. Opening a new
image clears the operation. Both edge methods always use the loaded original:
selecting Gaussian Smoothing followed by Canny does not chain the two operations.

## 22. Edge Algorithms: `processing/edges.py`

Both functions accept an unsigned 8-bit grayscale or BGR image. They use the
existing `grayscale()` helper and return a new two-dimensional `uint8` array with
the original height and width. Values are 0 for background and 255 for edges.
The original array is not modified. Existing preview conversion, histogram
computation, and full-resolution saving already support this representation.

### `sobel_edges(image, kernel_size=3, mean_ratio=1)`

The function validates the kernel and ratio, converts to grayscale, and computes
horizontal and vertical derivatives with `cv2.Sobel`. The derivative orders are
`(1, 0)` and `(0, 1)`. Using `cv2.CV_64F` retains negative derivatives and values
larger than 255; converting to unsigned pixels here would lose information.

`np.hypot(horizontal, vertical)` computes the gradient magnitude:

```text
magnitude = sqrt(horizontal² + vertical²)
threshold = mean_ratio × mean(magnitude across the whole image)
edge pixel = 255 if magnitude > threshold, otherwise 0
```

The mean is the mean of gradient magnitudes, not the original pixel intensities.
Thresholding happens before clipping or display conversion. For example, if the
mean magnitude is 40 and the ratio is 1.5, magnitudes above 60 become white;
a magnitude exactly equal to 60 remains black.

Both dark-to-light and light-to-dark boundaries can become edges because magnitude
uses the squared derivatives. Increasing the ratio with the same kernel can only
retain the same or fewer edge pixels. Ratio zero selects all nonzero gradients.
On a constant image both derivatives and the threshold are zero; the strict `>`
comparison keeps the result black rather than marking every pixel as an edge.

### `canny_edges(image, threshold_1=100, threshold_2=200, aperture_size=3)`

The function validates both thresholds and the aperture, checks that threshold 1
is no greater than threshold 2, then calls `cv2.Canny` on the grayscale image.
The aperture controls the derivative neighborhood size.

Canny thins gradient responses and uses two thresholds: strong candidates above
the upper threshold can start edges, while weaker candidates between thresholds
are retained when connected to strong edges. Isolated weak candidates are removed.
This is why its output can differ from Sobel's direct magnitude thresholding.

The call leaves `L2gradient` at OpenCV's default `False`, using the L1 gradient
measure (`|horizontal| + |vertical|`) rather than Sobel's Euclidean magnitude.
The application adds no Gaussian smoothing step before Canny. Equal thresholds
are allowed; reversed thresholds are rejected with a clear message rather than
silently reordered.

## 23. Edge Parameter Validation and Range Choices

| Parameter | Default / accepted values | Reason |
| --- | --- | --- |
| Sobel kernel size | 3; choices 3, 5, 7 | Project choice providing a small set of useful derivative neighborhoods. This is not Sobel's full supported range. |
| Sobel mean ratio | 1; finite numbers 0–10 | One thresholds at the mean gradient magnitude. Zero includes every nonzero gradient. The upper bound is a project demonstration limit, not an OpenCV constraint. |
| Canny threshold 1 | 100; finite numbers 0–255 | Lower gradient threshold. The range/default are project choices. |
| Canny threshold 2 | 200; finite numbers 0–255 | Upper gradient threshold; must be at least threshold 1. Gradient magnitudes can exceed 255, so this range is not OpenCV's maximum. |
| Canny aperture | 3; choices 3, 5, 7 | Matches the supported aperture sizes for this Canny call. Larger apertures change gradient strength and may require different thresholds. |

`validate_edge_size(value, name)` converts the value to stripped text and accepts
only `"3"`, `"5"`, or `"7"`, returning an integer. It also validates direct function
calls, even though normal GUI dropdown use already constrains these choices.
Values such as `3.0`, `4`, empty text, or `abc` raise `ValueError` with the supplied
parameter name. This validator is separate from M4's odd kernel range of 3–31.

Ratios and thresholds reuse `validate_number()` to reject empty, nonnumeric,
nonfinite, and out-of-range input. Canny additionally rejects reversed threshold
ordering. All parameter checks happen before the image-processing calls.

The existing coordinator catches validation errors and shows a warning. It catches
OpenCV errors separately and shows a processing-failed message. In either case,
the previous pixels and applied-result label remain intact. Correcting the values
and pressing Apply retries normally. No image uses the existing no-image warning.
M5 adds no resource handles or scheduled callbacks requiring additional cleanup.
