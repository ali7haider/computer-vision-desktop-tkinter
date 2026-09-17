# Beginner’s Guide to the Code

This guide explains how the application works for someone who is new to Python,
Tkinter, and computer vision. Start with sections 1–5, then follow an image through
opening, processing, and saving. You do not need to understand every OpenCV detail
on your first reading.


## 1. What does this application do?

The application lets you open a picture, choose an image operation, see the result,
and save it. You can also take a webcam snapshot and use it like an opened picture.

Here is the main journey:

```text
Start the application
    → Open an image or take a snapshot
    → Choose an operation
    → Adjust its settings
    → View the result
    → Save the result
    → Close the application
```

**The most important behavior to remember:** each image-changing operation starts
from the original image. Effects do not build on the previous result.

For example, choosing Grayscale and then Canny does not pass the grayscale result
from the first operation into the second. Canny receives the original and performs
its own grayscale conversion. Clicking Apply twice with the same settings does
not apply the effect twice as strongly.

Histogram is different: it measures the result currently displayed and does not
replace that result.

## 2. Words you will see in the code

| Word | Simple meaning | Example in this project |
| --- | --- | --- |
| Function | A named set of instructions that performs a task. | `load_image(path)` reads an image. |
| Argument | A value you give a function when calling it. | The filename passed to `load_image`. |
| Parameter | A named input in a function definition; also a setting in the interface. | `kernel_size` controls a filter’s neighborhood size. |
| Return value | The answer a function gives back. | `grayscale(image)` returns a grayscale image. |
| Module | A Python file that other files can import. | `processing/color.py`. |
| Class | A definition that groups related data and functions. | `ComputerVisionApp`. |
| Object | One instance created from a class. | `Webcam()` creates a camera-management object. |
| Method | A function belonging to a class. | `self.reset_image()`. |
| Attribute | A value stored on an object. | `self.current_image`. |
| State | The information the application remembers right now. | The original image and whether the webcam is running. |
| GUI | Graphical user interface: windows, buttons, and other visible controls. | The control panel and image preview. |
| Widget | One GUI element. | A button, textbox, or canvas. |
| Callback | A function registered to run when something happens. | Clicking Save As calls `save_image`. |
| Validation | Checking a value before using it. | Rejecting `abc` as a kernel size. |
| Exception | Python’s way of reporting that an operation could not finish normally. | `ValueError` for an invalid setting. |

Three tools do most of the work:

* **Tkinter** creates the interface and reacts to user actions.
* **NumPy** stores and calculates with grids of pixel numbers.
* **OpenCV**, imported as `cv2`, provides image-processing and camera functions.

## 3. Which file should I read?

| File | What it does |
| --- | --- |
| [main.py](../main.py) | Starts the application. Read this first. |
| [app.py](../app.py) | Connects user actions to processing, remembers images, and updates the screen. |
| [gui/layout.py](../gui/layout.py) | Builds menus, panels, preview area, and histogram window. |
| [gui/controls.py](../gui/controls.py) | Builds the operation dropdown and the settings for each operation. |
| [core/file_handler.py](../core/file_handler.py) | Reads images from files and writes results to files. |
| [core/webcam.py](../core/webcam.py) | Opens the camera, reads frames, and releases it. |
| [processing/color.py](../processing/color.py) | Changes grayscale, brightness, contrast, and color channels. |
| [processing/statistics.py](../processing/statistics.py) | Counts brightness levels and performs histogram equalization. |
| [processing/filters.py](../processing/filters.py) | Smooths or sharpens images. |
| [processing/edges.py](../processing/edges.py) | Finds edges using Sobel and Canny. |
| [processing/segmentation.py](../processing/segmentation.py) | Creates black-and-white masks and draws object boundaries. |
| [utils/validators.py](../utils/validators.py) | Checks processing settings before OpenCV receives them. |

The small `__init__.py` files mark folders as Python packages, allowing imports
such as `from processing.color import grayscale`. They contain descriptions rather
than application setup logic. `requirements.txt` lists the OpenCV and NumPy
dependencies; `.gitignore` keeps local environment and cache files out of Git.

Notice the division of work: the GUI creates controls, `app.py` decides what to do,
and `processing/` performs calculations. A processing function does not need to
know which button caused it to run.

## 4. How does the program start?

In `main.py`, the key lines are:

```python
root = tk.Tk()
ComputerVisionApp(root)
root.mainloop()
```

Read them as:

1. Create the main window and call it `root`.
2. Create the application object, giving it that window.
3. Keep listening for actions such as clicks, resizing, and closing.

The third step is called the **event loop**. The program waits for an event,
runs its callback, and then continues listening.

The last lines of `main.py` use:

```python
if __name__ == "__main__":
    main()
```

This means “start the application when this file is run directly.” Importing
`main.py` from another Python file does not automatically open the window.

### Understanding `self` and `__init__`

`ComputerVisionApp` is the main application class. Its `__init__` method runs when
the object is created. It sets up the window, initial values, controls, and callbacks.

Inside a method, `self` means “this particular application object.” For example,
`self.current_image` is the image remembered by this application. Storing it on
`self` lets different methods access it later.

### Why is there sometimes no `()` after a function name?

```python
command=on_open
```

This gives Tkinter a function to call **later**, when the user clicks the menu item.
Writing `command=on_open()` would call it immediately while building the interface.
That is why callbacks are usually passed without parentheses.

## 5. How does Python store an image?

A picture consists of tiny dots called **pixels**. This application stores their
values in a NumPy array: a grid of numbers.

A grayscale image stores one brightness number per pixel:

```text
0 = black        128 = medium gray        255 = white
```

A color image stores three numbers per pixel. OpenCV uses **BGR** order:
blue first, then green, then red.

```text
BGR [0, 0, 255]   = red
BGR [255, 0, 0]   = blue
BGR [255,255,255] = white
```

An image’s `shape` describes its dimensions. A color image with width 640 and
height 480 has shape `(480, 640, 3)`: height, width, number of channels. A grayscale
version has shape `(480, 640)`.

`uint8` means each stored value is a whole number from 0 to 255. Some calculations
use decimal or signed numbers temporarily, then convert back to `uint8`.

### The original, the result, and the preview

These names in `app.py` have different jobs:

| Attribute | What it remembers |
| --- | --- |
| `current_image` | The original image from a file or snapshot. |
| `display_image` | The full-size result that can be saved. |
| `preview_photo` | A Tkinter-compatible picture drawn inside the window. |
| `preview_status` | Text describing the result currently shown. |

Before an image exists, the image attributes are `None`, which means “no value yet.”

Reset uses:

```python
self.display_image = self.current_image.copy()
```

`.copy()` creates separate pixel storage. Without it, two variable names could
refer to the same array, so modifying pixels through one name could also affect
the other. Keeping the original separate makes Reset possible.

The preview may be smaller than the full-size result. Shrinking the window does
not shrink the image that Save As writes.

## 6. How are the interface and controls connected?

`create_layout()` in `gui/layout.py` creates the File and Tools menus, the left
control panel, and the right preview panel. It returns the preview canvas, control
panel, and two camera buttons so `app.py` can use them.

A **canvas** is a widget you can draw on. The preview canvas displays the image;
the histogram canvas displays bars and labels.

The layout uses `grid`, which places widgets in rows and columns. For example,
`sticky="nsew"` lets a widget stretch toward all four sides of its cell, and
`weight=1` lets a row or column receive extra space. This makes the preview grow
when the window grows. The initial window is 1000×650, with a minimum of 700×450.
On macOS, File and Tools appear in the system menu bar at the top of the screen.

`OperationControls` in `gui/controls.py` manages the left panel:

| Method or value | Purpose |
| --- | --- |
| `OPERATIONS` | The names of all thirteen operations, shared with the Tools menu. |
| `choose(operation)` | Remove the old parameter widgets and create the selected operation’s defaults. |
| `add_slider(...)` | Create a slider for a numeric setting. |
| `add_entry(...)` | Create a textbox. |
| `add_choice(...)` | Create a dropdown of allowed settings. |
| `set_image_loaded(loaded)` | Enable or disable parameter controls. |
| `get_parameters()` | Read current values into a dictionary. |

A **dictionary** stores names with their values. For Median Filter, parameters
might be `{"kernel_size": "3"}`. Textboxes return text, even when you type a number;
validation converts that text before processing.

`StringVar` and `DoubleVar` are Tkinter values connected to widgets: text and
numbers respectively. Calling `.get()` reads the value; `.set(...)` changes it.
`values` stores these variables, while `sliders`, `entries`, and `choices` store
widget references so their enabled/disabled state can be updated.

In the Tools menu, `lambda name=operation: on_select(name)` creates a short
callback. The `name=operation` part remembers the correct name for each menu item.

## 7. What happens when I open an image?

```text
File → Open...
    → app.py: open_image()
    → show file picker
    → core/file_handler.py: load_image(path)
    → remember the original
    → clear operation selection and reset the result
    → draw the preview
```

`load_image()` performs these checks and steps:

1. `validate_extension()` checks for `.jpg`, `.jpeg`, `.png`, or `.bmp`, ignoring case.
2. `np.fromfile()` reads the file’s bytes. This also supports Unicode filenames.
3. An empty file is rejected.
4. `cv2.imdecode()` turns those bytes into pixels.
5. If decoding fails, the helper reports an error rather than returning an image.

The file extension alone is not proof of a valid image. Renaming a text file to
`photo.jpg` does not make it readable as a photograph.

`cv2.IMREAD_COLOR` loads a three-channel BGR image. Even a grayscale file becomes
a three-channel image when opened; PNG transparency is not preserved. Saving later
writes pixel content rather than preserving the original file’s metadata.

If you cancel the picker, nothing changes. If opening fails, the application
shows “Open Failed” and keeps the previous image. It only replaces image state
after loading succeeds. A successful open also stops any live webcam capture.

## 8. What happens when I choose an operation?

`select_operation()` in `app.py` cancels any waiting processing update, rebuilds
the controls with default settings, and calls `apply_operation()`.

```text
apply_operation()
    → check that a static image is available
    → read the selected operation and parameters
    → call the matching processing function
    → store its returned image in display_image
    → update the result label, preview, and any open histogram
```

The method uses `if` and `elif` branches to choose a function. For example:

```python
result = median_filter(self.current_image, **parameters)
```

Here `**parameters` passes the dictionary entries as named arguments. If the
dictionary is `{"kernel_size": "3"}`, the call means:

```python
result = median_filter(self.current_image, kernel_size="3")
```

The processing function validates the setting and returns a new result. Only after
it succeeds does `app.py` replace `display_image`. An invalid setting therefore
leaves the previous result and its label intact.

### When do edited settings take effect?

| User action | Result |
| --- | --- |
| Select an operation | Apply its default settings immediately, if an image is loaded. |
| Move a slider | Schedule an automatic update after about 40 milliseconds. |
| Edit a textbox or parameter dropdown | Wait for Apply. |
| Click Apply | Read the current settings and process immediately. |
| Click Reset | Restore the original and default settings; keep the selected operation. |
| Open another image or take a snapshot | Use a new original and clear operation selection. |

Reset does not automatically reapply the selected effect. Its label says the
original is shown.

The result label describes **successfully applied values**. If Median Filter was
applied with size 3 and you type 5, the label stays at 3 until Apply succeeds.
Typing `abc` and clicking Apply produces a warning and keeps the size-3 result.

## 9. Color and brightness operations

These functions are in `processing/color.py`.

### Grayscale: `grayscale(image)`

Grayscale removes color and keeps brightness information. The function uses
`cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`. It combines the color channels with
weights; it does not simply average all three equally. If the input is already
grayscale, the function returns a copy.

The result has one number per pixel instead of three.

### Brightness / Contrast: `brightness_contrast(...)`

The calculation is:

```text
new value = old value × contrast + brightness
```

Brightness adds or subtracts an amount. Contrast multiplies the value. Defaults
of brightness 0 and contrast 1 leave the image unchanged.

For a channel value of 100, contrast 1.5 and brightness 20 give:

```text
100 × 1.5 + 20 = 170
```

The code temporarily uses decimal numbers to avoid overflowing the 0–255 storage
range. `np.rint()` rounds, and `np.clip()` limits the answer to 0–255. For example,
300 becomes 255 and −20 becomes 0. The result is then converted back to `uint8`.

### RGB Channels: `rgb_channels(...)`

Each color gets its own multiplier, also called a gain:

* 0 removes that channel.
* 1 leaves it unchanged.
* 2 doubles it, limited to 255.

The controls say Red, Green, Blue, but the code builds gains in `[blue, green, red]`
order to match OpenCV. With a red gain of 0, a BGR pixel `[20, 40, 100]` becomes
`[20, 40, 0]` if the other gains stay at 1.

## 10. Histogram and histogram equalization

These functions are in `processing/statistics.py`.

### Histogram: `compute_histogram(image)`

A histogram counts how many pixels have each brightness value. There are 256
possible values, from 0 through 255, so there are 256 counts, or **bins**.

For the tiny grayscale image `[0, 0, 128, 255]`:

```text
Brightness 0:   2 pixels
Brightness 128: 1 pixel
Brightness 255: 1 pixel
All other brightness values: 0 pixels
```

`cv2.calcHist()` calculates the counts after grayscale conversion. `.ravel()`
turns its result into a simple one-dimensional array of counts.

Histogram uses `display_image`, so it describes the current result. It does not
change the picture. In the chart, the horizontal axis is brightness and the
vertical axis is the number of pixels.

`show_histogram()` opens or reuses a separate window. `update_histogram()` refreshes
it when the result changes. `create_histogram_window()` builds that window, and
`display_histogram()` draws the supplied counts without doing image processing.
Resizing redraws the chart; the old resize callback is removed when counts change.
If you close the histogram, selecting Histogram again creates a new window.

### Histogram Equalization: `equalize_histogram(image)`

This converts the original to grayscale and calls `cv2.equalizeHist()`. It remaps
brightness values using their distribution, which can make details easier to see
when many pixels occupy a narrow brightness range.

The output is grayscale, even when the original is colored. Equalization is not
a guarantee that every picture will look better or that all histogram bars will
have equal heights.

## 11. Smoothing and sharpening filters

These functions are in `processing/filters.py`.

A **neighborhood** is a small area around a pixel. A **kernel** is the small window
or matrix used to calculate a new value from that area. Size 3 means a 3×3 area:

```text
neighbor  neighbor  neighbor
neighbor   center   neighbor
neighbor  neighbor  neighbor
```

Odd sizes give the window a clear middle pixel.

### Median Filter: `median_filter(image, kernel_size=3)`

The median is the middle value after sorting. For `[10, 11, 250]`, it is 11.
A median filter uses neighborhood medians to reduce isolated bright or dark spots.
The implementation calls `cv2.medianBlur()`; color channels are processed separately.

A larger neighborhood can remove more small details along with noise.

### Gaussian Smoothing: `gaussian_smoothing(image, kernel_size=5, sigma=0)`

This blurs the image using a weighted average. Nearby pixels receive more weight
than distant pixels. The implementation calls `cv2.GaussianBlur()`.

Kernel size controls the neighborhood width and height. **Sigma** controls the
spread of the weights. Sigma 0 asks OpenCV to choose a value based on kernel size.

### Sharpening: `sharpen(image)`

Sharpening emphasizes differences between nearby pixels using this fixed matrix:

```text
 0  -1   0
-1   5  -1
 0  -1   0
```

For an interior pixel, this means five times the center minus its top, bottom,
left, and right neighbors. If all five values are 100, the answer is still 100.
If the center is 120 and its four neighbors are 100, the answer is 200, making
the difference stronger.

`cv2.filter2D(image, -1, kernel)` performs the calculation. `-1` keeps the output
pixel type the same as the input. Values outside the byte range are limited to
that range. Sharpening has no editable settings in this application.

## 12. Finding edges

These functions are in `processing/edges.py`. An **edge** is a place where brightness
changes sharply, such as the boundary between a dark object and a bright background.
Both methods return a grayscale-sized image containing only 0 and 255: black
background and white detected edges.

### Sobel: `sobel_edges(image, kernel_size=3, mean_ratio=1)`

Sobel measures brightness changes in horizontal and vertical directions. Those
measurements are called **gradients**. The code combines them into an edge strength:

```text
strength = sqrt(horizontal² + vertical²)
threshold = mean ratio × average strength across the image
strength > threshold → white
otherwise → black
```

`sqrt` means square root. `np.hypot()` calculates this combined strength.
`cv2.CV_64F` allows the intermediate gradients to contain negative and large values;
using 0–255 storage too early would lose information.

For example, average strength 40 and ratio 1.5 give a threshold of 60. Strength
70 becomes white; strength 60 remains black because the comparison is strictly
“greater than.” The average is calculated from gradients, not original brightness.

Increasing the ratio keeps the same or fewer edges with the same kernel. Ratio 0
keeps all nonzero gradients. A constant image stays black because it has no changes.

### Canny: `canny_edges(image, threshold_1=100, threshold_2=200, aperture_size=3)`

Canny uses a lower and an upper threshold. Strong edge candidates can start edges;
weaker candidates are kept when connected to strong ones. It also thins edge
responses. This usually gives a different result from directly thresholding Sobel
strengths.

**Aperture size** is the neighborhood size used for calculating derivatives.
Threshold 1 must be less than or equal to threshold 2; reversed values cause a
warning. Equal thresholds are allowed.

The function calls `cv2.Canny()` on a grayscale version of the original. This
application adds no separate Gaussian smoothing step before that call. It leaves
OpenCV’s `L2gradient` option at its default `False`, which uses
`|horizontal| + |vertical|` for gradient strength; the bars mean absolute value.

## 13. Selecting regions and drawing boundaries

These functions are in `processing/segmentation.py`. **Segmentation** means
separating an image into regions. Here, a **binary mask** is a black-and-white image
where white marks selected pixels, called foreground, and black marks background.

### Global Thresholding: `global_threshold(image, threshold=127)`

A single brightness cutoff is used for the whole grayscale image:

```text
brightness > threshold → 255 (white)
brightness ≤ threshold → 0 (black)
```

At threshold 127, `[126, 127, 128]` becomes `[0, 0, 255]`. At threshold 255,
everything is black. The implementation uses `cv2.threshold()` with `THRESH_BINARY`.

### Adaptive Thresholding: `adaptive_threshold(...)`

Adaptive thresholding chooses a local cutoff around each pixel instead of using
one cutoff everywhere. This can help with uneven lighting.

Its three settings are:

* **Block size:** the width and height of the neighborhood, such as 11×11.
* **Method:** Mean uses a simple average; Gaussian gives nearby pixels more weight.
* **Constant C:** an amount subtracted from that local average.

For example, a local average of 100 and C of 2 give a conceptual threshold of 98.
A larger C lowers the cutoff and generally selects more foreground. A negative C
raises it. OpenCV uses integer-pixel rounding, so small fractional changes can
produce the same result.

The code calls `cv2.adaptiveThreshold()` and returns a binary mask. OpenCV handles
image borders by repeating border pixels, so the block can be larger than the image.

### Contour Detection: `detect_contours(image, threshold=127)`

A **contour** follows the boundary of a selected region. This function:

1. Calls `global_threshold()` to select bright regions.
2. Uses `cv2.findContours()` to find their outer boundaries.
3. Makes a color copy of the original.
4. Draws the boundaries in green using `cv2.drawContours()` with thickness 2.

`RETR_EXTERNAL` means only outer boundaries are retrieved, so holes inside objects
are not outlined. `CHAIN_APPROX_SIMPLE` saves straight portions using fewer points.
The `-1` passed to `drawContours()` means “draw all retrieved contours.”

The result is a color image with green outlines, not a black-and-white mask. If
nothing is selected, no outlines appear. There is no minimum-area filter. Because
bright regions are selected, a dark object on a bright background may lead to an
outline of the surrounding bright region instead.

## 14. Which settings are accepted?

A **default** is the starting value shown when selecting an operation. Ranges below
are this project’s accepted settings; they are not all universal OpenCV limits.

| Operation | Setting | Default | Accepted values |
| --- | --- | --- | --- |
| Brightness / Contrast | Brightness | 0 | −255 to 255 |
| Brightness / Contrast | Contrast | 1 | 0 to 3 |
| RGB Channels | Each color gain | 1 | 0 to 2 |
| Median Filter | Kernel size | 3 | Odd integers from 3 to 31 |
| Gaussian Smoothing | Kernel size | 5 | Odd integers from 3 to 31 |
| Gaussian Smoothing | Sigma | 0 | 0 to 10; 0 means automatic |
| Sobel | Kernel size | 3 | 3, 5, or 7 |
| Sobel | Mean ratio | 1 | 0 to 10 |
| Canny | Threshold 1 | 100 | 0 to 255, no greater than threshold 2 |
| Canny | Threshold 2 | 200 | 0 to 255 |
| Canny | Aperture size | 3 | 3, 5, or 7 |
| Global Thresholding / Contour Detection | Threshold | 127 | 0 to 255 |
| Adaptive Thresholding | Block size | 11 | Odd integers from 3 to 31 |
| Adaptive Thresholding | Constant C | 2 | −50 to 50 |
| Adaptive Thresholding | Method | Gaussian | Mean or Gaussian |

Brightness and threshold sliders move in steps of 1; contrast and color gains
move in steps of 0.05. Grayscale, Histogram, Histogram Equalization, and Sharpening
have no editable parameters.

The 31 limit for filter/block sizes, 10 limit for sigma and Sobel ratio, and ±50
range for C are practical project choices. Canny’s thresholds measure gradients,
which can exceed 255; the chosen 0–255 range is not OpenCV’s maximum. The edge-size
validator restricts Sobel to a small selection and Canny to supported aperture sizes.

### How validation works

`utils/validators.py` provides three helpers:

| Helper | What it checks |
| --- | --- |
| `validate_number()` | Convert to a number, reject infinity/NaN, and check minimum and maximum. |
| `validate_kernel_size()` | Require whole-number text representing an odd size from 3 to 31. |
| `validate_edge_size()` | Accept only `3`, `5`, or `7` and return an integer. |

NaN means “not a number”; infinity is not a usable finite setting. Kernel validation
rejects inputs such as an empty string, `abc`, `3.5`, `4`, `0`, and `33`. It also
rejects decimal spelling such as `3.0` and text longer than two digits. The optional
`name` argument lets the same helper say “Block size” for adaptive thresholding.

Canny checks threshold ordering, and adaptive thresholding checks the method name
inside their processing functions. These checks also apply when a function is
called directly rather than through the GUI.

When validation raises `ValueError`, `app.py` shows an “Invalid Parameter” warning
and returns to waiting for user input. The previous result remains available.
`require_image()` similarly warns if no image is available or live capture is active.

## 15. How is the preview drawn and kept responsive?

`refresh_preview()` chooses `latest_frame` during live capture or `display_image`
otherwise. With no image, it displays a message inviting you to open an image or
access the webcam.

To fit a picture in the canvas, it calculates:

```python
scale = min(width / image_width, height / image_height, 1.0)
```

Both dimensions use the same scale, so the picture keeps its proportions. The
`1.0` prevents enlarging small images. For a 1600×900 image inside an 800×600 area,
the preview becomes 800×450, while the saved image remains 1600×900.

The method resizes with `cv2.INTER_AREA`, converts BGR or grayscale to RGB, and
creates PPM image data. **PPM** is a simple image format Tkinter can read directly,
so no additional image-display library is needed.

`tk.PhotoImage` creates the displayable object. The application keeps it in
`self.preview_photo`; otherwise Python could remove the object while the canvas
still needs it. The canvas draws it in the center. Dimension checks keep very
small or thin previews at least one pixel wide and high.

### What does `after(40, ...)` mean?

It asks Tkinter to run a function after about 40 milliseconds. It does not pause
the current function for that time or create another thread.

| Stored job identifier | Scheduled work |
| --- | --- |
| `resize_job` | Redraw after a canvas size change. |
| `processing_job` | Recalculate after a slider change. |
| `webcam_job` | Read and show the next webcam frame. |

An identifier lets the application cancel a waiting callback. `None` means no job
is waiting. `schedule_preview()` and `schedule_operation()` keep only one waiting
update of each kind. More resize/slider events leave that update in place; when
it runs, it uses the latest dimensions or settings. This avoids a growing queue
of repeated work while allowing updates during continuous dragging.

The delay is approximate. A busy event loop may run the callback later.
`cancel_processing()` removes pending processing when selecting, applying,
resetting, starting capture, or closing.

## 16. What happens when I save?

The Save As button and File → Save As call the same `app.py` method:

```text
Check that a static result exists
    → copy display_image
    → ask for a destination filename
    → encode the copied pixels as PNG, JPEG, or BMP
    → write the file
```

The method warns if no image is loaded or the webcam is live. The default extension
is `.png`. Cancelling the dialog writes nothing.

There are two functions named `save_image`: the method in `app.py` handles the user
action; the helper `save_image(path, image)` in `core/file_handler.py` writes pixels.
The helper checks the extension, calls `cv2.imencode()`, checks its success flag,
and writes the resulting bytes with `.tofile()`.

### Why copy before showing the dialog?

A native save dialog can allow waiting Tkinter callbacks to run. For example, a
slider update might change the result while you choose a filename. Copying first
ensures the saved pixels are the result shown when you requested Save As. This is
the M8 save-timing fix.

Saving uses the full-size result, not the smaller preview. PNG and BMP preserved
pixel values in recorded checks; JPEG compression can change values slightly.
All retained full image dimensions in those checks.

Encoding happens before the destination is opened, so an encoding failure does
not erase an existing file. A failure while writing can still leave a partial
file; the application reports expected write errors.

## 17. How does the webcam work?

`Webcam` in `core/webcam.py` handles the device. It does not draw windows.

| Method | What it does |
| --- | --- |
| `start()` | Release any old camera handle, open the default camera with `cv2.VideoCapture(0)`, and check it opened. |
| `read()` | Read one frame; reject a failed read, missing frame, or empty frame. |
| `stop()` | Clear the stored handle and call `release()` if a camera is open. |

A **frame** is one picture from the video stream. A **handle** is the object used
to communicate with the camera. Releasing it tells the system this application is
finished using the device. Repeated stops do nothing once the handle is cleared.
Expected opening/reading failures also trigger cleanup.

`app.py` controls how frames appear:

```text
start_webcam()
    → open camera and read the first frame
    → remember the previous result label
    → enter live mode and show camera buttons
    → display the frame
    → schedule update_webcam() after about 30 ms

update_webcam()
    → read and show another frame
    → schedule the next update
```

The camera object is stored in `webcam`. `webcam_running` tells the application
whether live mode is active, and `latest_frame` holds the latest full-size camera
image. `static_status` remembers the previous static result’s label.

The original and processed static images stay in memory during capture. Starting
the webcam disables processing controls and closes an existing histogram, since
it would describe the old static result. No video or image is saved automatically.

Camera reads run in the same Tkinter event loop as the interface. The 30 ms delay
is not a guaranteed frame rate, and slow camera reads can affect responsiveness.

### Snapshot versus Stop

`take_snapshot()` copies the latest frame, stops the camera, and makes that copy
the new original. It clears operation selection and resets the displayed result.
The snapshot can then be processed and saved just like an opened file.

`stop_webcam()` cancels the frame callback, releases the camera, clears live state,
and restores the previous static result and label. It re-enables appropriate
controls. If there was no previous image, the empty preview returns.

The Take Snapshot and Stop Webcam buttons are shown only during live capture.
`grid_remove()` hides their containing frame without forgetting its placement;
`grid()` shows it again next time.

| Action during live capture | Behavior |
| --- | --- |
| Apply, Reset, select an operation, or Save As | Show a reminder to take a snapshot or stop first. |
| Successfully open a file | Stop the webcam and use the opened image. |
| Cancel Open or choose an unreadable file | Keep capture running. |
| Camera read fails | Stop and release the camera, restore the static view, and show an error. |
| Start again while already running | Keep the existing capture; do not open another. |
| Close the application | Cancel callbacks and release the camera. |

## 18. How are errors and closing handled?

Expected mistakes should lead to a clear message and a usable application.

```text
Detect the problem → show feedback → return safely → wait for another action
```

The helpers report problems with exceptions; `app.py` decides which dialog to show.
For file actions it catches `OSError` (file access problems), `ValueError` (invalid
content or extension), and `cv2.error` (OpenCV failures). Processing handles invalid
parameters and OpenCV errors; reading invalid Tkinter slider values handles
`tk.TclError`. These are specific expected error types, rather than a catch-all
that could hide unrelated programming bugs.

| Example | Intended response |
| --- | --- |
| Apply with no image | Ask the user to open an image. |
| Apply with no selected operation | Ask the user to choose an operation. |
| Invalid filter size | Show a warning and preserve the last successful result. |
| Corrupt or unreadable image | Show Open Failed and keep the current image. |
| Unwritable save location | Show Save Failed and keep the in-memory result. |
| Unavailable webcam | Show an error and preserve the static image. |
| Snapshot without an active frame | Ask the user to start the webcam first. |

Both File → Exit and the window’s close button call `close()`. It cancels pending
processing, stops the webcam, cancels a pending preview update, and calls
`root.destroy()`. This closes the main window and histogram window and allows
`mainloop()` to finish. Cancelling jobs first prevents them from later trying to
update widgets that have been destroyed.

The recorded checks and their limits are in the progress tracker. Camera checks
performed by the agent used simulated cameras; physical camera behavior was not
independently tested by the agent. Initial clipping of the native macOS Save As
dialog remains a recorded unresolved UI issue. The current code keeps the native
dialog attached to the main window with `parent=self.root`.

## 19. Follow one complete example through the code

Suppose you open `photo.png`, apply Median Filter with size 5, and save `result.png`:

1. `main.py` creates the window and starts the event loop.
2. File → Open calls `ComputerVisionApp.open_image()`.
3. `load_image()` reads and decodes the file into BGR pixel numbers.
4. The app stores the original in `current_image` and a copy in `display_image`.
5. `refresh_preview()` draws a fitted version of that copy.
6. Selecting Median Filter creates its controls and applies the default size 3.
7. You type 5 and click Apply. `get_parameters()` returns `{"kernel_size": "5"}`.
8. `median_filter()` validates 5 and runs `cv2.medianBlur()` on the original.
9. The app stores the returned result in `display_image` and updates the label.
10. Save As copies that full-size result before asking for a filename.
11. The file helper encodes the copy as PNG and writes `result.png`.
12. Closing cancels pending work, releases any camera, and destroys the window.

If you type `abc` at step 7, validation stops that attempt. The size-3 result stays
visible, and you can correct the value and try again.

To trace another feature, follow the same route: find its name in
`gui/controls.py`, find its branch in `app.py`, then read the corresponding function
in `processing/`. This connects what you see on the screen to the code that does
the work.
