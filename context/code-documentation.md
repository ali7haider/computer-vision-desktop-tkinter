# Code Documentation

This guide explains how the verified application works, so the student can trace
the code and explain it during evaluation. It covers **M1 and M2**:

* M1 foundation: commit `3b953a0`.
* M2 image loading, preview, and saving: commit `b0c57a2`.

The explanations below describe the implementation at the end of M2. M3 color
and statistics operations are not included. Update this guide after user
verification, before committing future implementation changes.

For installation and manual checks, see [README](../README.md). For verification
results and milestone status, see the [progress tracker](planning/progress-tracker.md).

## 1. Code Map

| File | Responsibility |
| --- | --- |
| `main.py` | Create the Tkinter root, create the application, start the event loop. |
| `app.py` | Own image state and connect file actions, preview updates, and shutdown. |
| `gui/layout.py` | Create menus, arrange panels, and return the preview canvas. |
| `gui/controls.py` | Create the operation controls, disabled through M2. |
| `core/file_handler.py` | Validate file extensions, decode images, and encode/save images. |
| Package `__init__.py` files | Mark `gui`, `core`, `processing`, and `utils` as regular Python packages. |
| `requirements.txt` | Declare OpenCV 4.x and NumPy 2.x dependency ranges. |
| `.gitignore` | Exclude Python cache files and the local `.venv` environment from Git. |

`processing` and `utils` contain only package markers in the committed M2 code.
Webcam and processing implementations belong to later milestones.

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
`self.save_image`. These are **callbacks**: functions to call later.

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

The constructor also binds canvas `<Configure>` events to `schedule_preview` and
the window-close protocol `WM_DELETE_WINDOW` to `close`.

### Original, result, and preview are different things

After loading, the code assigns:

```python
self.current_image = image
self.display_image = image.copy()
```

`.copy()` gives the result its own pixel storage. Assigning `display_image = image`
would make both names refer to the same array; later edits through one reference
could change the other. M2 gives both arrays identical content but separate storage.

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

### `gui/layout.py`: `create_layout(root, on_exit, on_open, on_save)`

This function creates the File and Tools menus and attaches the menu bar with
`root.configure(menu=menu_bar)`.

At the end of M2:

* Open, Save As, and Exit have callbacks.
* Webcam, processing operations, and Reset menu actions are disabled.

On macOS, the active application's menus appear in the system menu bar at the top
of the screen. They do not appear as a row inside the application window.

The function uses `grid` to arrange the controls on the left and preview on the
right. `sticky="nsew"` lets a widget fill its grid cell in all directions.
Row/column `weight=1` allows a cell to receive extra space when its parent grows.
The preview column gets the extra horizontal space; the controls keep their
requested width.

The preview canvas starts with requested dimensions of `1×1`, allowing the grid
to determine its actual size. It has a white background. The function returns
this canvas so `app.py` can draw on it without placing file-handling logic in
the layout module.

### `gui/controls.py`: `create_controls(parent)`

This creates the operation label, disabled dropdown, parameter placeholder, and
disabled Apply/Reset buttons. These are deliberate placeholders in M1/M2, not
working processing actions. This function only constructs widgets.

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
It cancels a pending preview update, clears `resize_job`, and calls `root.destroy()`.

Cancelling first prevents delayed code from trying to redraw destroyed widgets.
Destroying the root closes the GUI and lets `mainloop()` return. M1/M2 do not open
a camera, so there are no webcam resources to release yet.

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
