# Progress Tracker

## Current Status

**M1 — Project Foundation: complete.**

Automated GUI checks passed, and the user confirmed M1 works.

**M2 — Image I/O + Basic GUI: complete.**

Automated checks passed, and the user confirmed manual verification, including
continuous preview updates during resizing.

**M3 — Color + Statistics: complete.**

User confirmed M3 works, including the revised Reset behavior. Code documentation
has been updated for the verified implementation.

**M4 — Filters + Local Operators: complete, including the applied-result label.**

## Current Task

M4 is verified and documented. User will create the commit and push; M5 is next.

## Completed

### Code Documentation

* Added `context/code-documentation.md` explaining the committed M1/M2 code,
  state, callback flow, preview conversion, resizing, file I/O, and error handling.
* Updated `AGENTS.md` to require code documentation after user verification,
  before implementation commits.

### Project Planning

* Reviewed the assignment and defined scope, architecture, code standards, UI rules, and build plan.
* Defined the no-crash principle and agent workflow.

### M1 — Project Foundation

* Added `main.py` to create the Tkinter root and run the event loop.
* Added `ComputerVisionApp` in `app.py` to coordinate the window and shutdown.
* Created `gui`, `core`, `processing`, and `utils` packages.
* Added GUI layout and controls modules; later feature modules will be added in their milestones.
* Added File and Tools menus, control panel, and expandable image preview.
* Disabled unfinished menu actions, operation selection, Apply, and Reset.
* Connected File → Exit and window close to application shutdown.

## Verification

### M1

Verified using Python 3.13.13 with Tk 8.6:

* Window and both panels are visible.
* File and Tools menus exist.
* Unfinished actions and controls are disabled.
* Layout fits at 700×450, 1000×650, and 1200×800; preview expands with the window.
* File → Exit and the window-close protocol callback both end the event loop without callback errors.
* Repeated creation and closing of the shell succeeds.

All eight Python files passed syntax parsing. Whitespace checks passed.

Automated checks ran against real Tk windows. The user confirmed M1 works on
2026-09-15, including locating File and Tools in the macOS system menu bar.

### M2

Implemented:

* File → Open... and File → Save As... with native Tkinter dialogs.
* JPG/JPEG, PNG, and BMP loading/saving, including Unicode filenames.
* Separate original/current and displayed/result image arrays.
* Centered preview that preserves proportions and fits the window.
* Preview updates during continuous resizing using one pending 40 ms callback.
* Full-resolution saving, independent of the resized preview.
* Clear feedback for invalid/unreadable files, save failures, and saving without an image.
* Cancelled dialogs and failed opens preserve the current image.
* Resize callbacks are cancelled on exit.
* Project virtual environment and minimal dependency requirements.

Verified with Python 3.13.13, Tk 8.6, OpenCV 4.12.0, and NumPy 2.2.6:

* 63 automated checks passed against temporary files and a real Tk window.
* JPG/PNG/BMP round trips, uppercase extensions, and Unicode filenames.
* PNG/BMP pixel equality; full dimensions retained for all tested formats.
* Correct red/blue preview colors, aspect ratio, and resizing at three window sizes.
* Full-resolution displayed result is saved while the original remains unchanged.
* Empty, corrupt, unsupported, and missing files produce errors safely.
* Open/Save cancellation, no-image save, repeated use, and recovery after errors.
* Invalid save destinations/extensions and simulated permission/OpenCV failures.
* Encoding failure leaves an existing destination untouched.
* Tiny, thin, and grayscale previews; close with a pending resize callback.
* All nine Python source files pass syntax parsing; dependency and whitespace checks pass.
* Follow-up resize check passed: 16 preview updates during a sequence of 30
  programmatic size changes, with updates before resizing stopped. Final fit,
  proportions, full image resolution, and closing with a pending update passed.

Dialog choices/messages and permission failures were simulated for automated checks.
The user confirmed manual verification on 2026-09-15. Individual manual test results
were not recorded. Processing and webcam controls were disabled at the end of M2.

### M3

Implemented:

* Grayscale conversion and grayscale histogram equalization.
* Live brightness/contrast sliders and independent RGB channel gains.
* A 256-bin grayscale intensity histogram for the displayed image, shown in a
  reusable, resizable Tkinter window and refreshed when the image changes.
* Tools actions, operation dropdown, Apply, and Reset.
* Adjustments recompute from the loaded original. Reset restores it and default
  slider values, keeping the selected operation without a confirmation prompt.
  Opening a new image clears selection and pending processing.
* Numeric validation rejects nonnumeric, nonfinite, and out-of-range parameters.
* Slider updates use one pending 40 ms callback; pending work is cancelled on exit.
* Existing histogram resize callbacks are removed before replacing them.

Verification:

* 126 M3 checks passed using known pixel examples, temporary files, and real Tk windows.
* After the Reset adjustment, 134 M3 checks passed, including keeping all operation
  selections, restoring slider defaults/original pixels, and clearing selection
  when opening a new image.
* Known grayscale values, brightness/contrast clipping, RGB channel ordering,
  histogram counts, and equalization mapping matched expected results.
* Normal, minimum, maximum, invalid, and nonfinite parameters were exercised.
* Every operation without an image gives feedback; sliders are disabled until loading.
* Live sliders, repeated Apply, reset, operation switching, new-image loading,
  unchanged originals, and full-resolution grayscale saving passed.
* Histogram reuse, closing/reopening, rendering, and callback cleanup passed.
* Controls fit at 700×450, 1000×650, and 1200×800.
* Invalid parameters and simulated OpenCV failures preserve the previous result.
* Closing with pending processing/preview work and an open histogram passed.
* All 63 M2 regression checks passed after M3 integration.
* Twelve Python source files passed syntax parsing; whitespace checks passed.

GUI actions were driven programmatically and dialogs simulated. The user confirmed
manual verification, including Reset; individual manual results were not recorded. No new dependencies
were added. Webcam remains disabled until M7.

## In Progress

No feature implementation in progress.

### M4 — Filters + Local Operators: Complete

User confirmed the filters and applied-result label work on 2026-09-16.

* Added median filtering, Gaussian smoothing, and fixed-kernel sharpening in
  `processing/filters.py`; eight operations are now available.
* Added kernel/sigma textboxes. Selection applies defaults; edited values run on Apply.
* Kernel validation accepts odd integers 3–31; sigma accepts finite numbers 0–10.
  Sigma 0 uses OpenCV's automatic choice. Invalid input preserves the displayed result.
* Reset keeps the operation, restores defaults and original pixels, and shows no prompt.
* Added a preview label showing the applied operation and parameter values.
  Open/Reset identify the original; pending edits, failed Apply, and histogram
  viewing preserve the label describing the displayed pixels.
* Focused GUI status checks passed for empty/original/applied states, parameter
  edits, invalid input, histogram, Reset, live sliders, and minimum window size.
* 111 M4 algorithm/GUI checks passed: known pixel cases, constant/tiny images,
  parameter boundaries, invalid inputs, disabled entries without an image,
  repeated use, Reset, histogram integration, and minimum-window layout.
* 137 M3/integration regression checks passed after adding the new operations.
* All 13 Python files passed syntax parsing; whitespace checks passed.
* Dialogs were simulated and GUI controls driven programmatically. User manual
  verification is confirmed; individual manual results were not recorded.
* Code documentation now covers filters, textbox flow, validation, parameter-range
  rationale, and the applied-result label.

## Blocked / Known Issues

* The default pyenv Python 3.11.7 lacks `_tkinter`.
* System Python 3.9.6 imports Tk but aborts on GUI launch with a macOS version compatibility error.
* `.venv` uses the working framework Python 3.13.13 and has OpenCV/NumPy installed.
  Run the application from the project directory:

```bash
.venv/bin/python main.py
```

The application contains no machine-specific paths. README.md includes environment setup
instructions. OpenCV is constrained to version 4.x to use compatible prebuilt packages.

## Pending

* M5: Edge detection.
* M6: Segmentation.
* M7: Webcam and snapshot.
* M8: Integration and stability.
* M9: Documentation and demo.

See `build-plan.md` for milestone scopes.

## Next Steps

1. User commits and pushes the verified M4 changes.
2. Proceed to M5 — Edge Detection when requested.

## Recent Changes

* Marked M4 complete after user verification and documented range choices,
  distinguishing OpenCV constraints from practical project limits.

* Implemented M4 filters, textbox controls, validation, and manual checklist.

* Marked M3 complete after user verification and updated code documentation,
  including live controls, algorithms, histogram lifecycle, and Reset behavior.

* Implemented M3's five operations and controls; passed M3 and M2 regression checks.
* Added M3 ranges, operation behavior, and manual verification instructions to README.md.

* Documented committed M1/M2 code and added the documentation workflow rule.

* Implemented and checked the M1 shell.
* Marked M1 complete after user verification.
* Removed stale tracker references to separate UI tokens and project skills, following `AGENTS.md`.
* Recorded runtime limitations and the working verification environment.
* Implemented M2 image I/O and preview; passed 63 automated checks.
* Added dependency setup and manual verification instructions to README.md.
* Replaced the resize pause with periodic updates after user feedback.
* Marked M2 complete after user verification; user will push the commit manually.

## Last Updated

2026-09-16
