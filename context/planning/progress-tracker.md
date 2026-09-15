# Progress Tracker

## Current Status

**M1 — Project Foundation: complete.**

Automated GUI checks passed, and the user confirmed M1 works.

**M2 — Image I/O + Basic GUI: complete.**

Automated checks passed, and the user confirmed manual verification, including
continuous preview updates during resizing.

## Current Task

Prepare the completed M2 changes for the user's manual push. M3 is next.

## Completed

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
were not recorded. Processing and webcam controls remain disabled.

## In Progress

No feature implementation in progress. M2 is complete; M3 has not started.

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

* M3: Color and statistics operations.
* M4: Filters and local operators.
* M5: Edge detection.
* M6: Segmentation.
* M7: Webcam and snapshot.
* M8: Integration and stability.
* M9: Documentation and demo.

See `build-plan.md` for milestone scopes.

## Next Steps

1. User pushes the completed M2 commit.
2. Proceed to M3 — Color + Statistics.

## Recent Changes

* Implemented and checked the M1 shell.
* Marked M1 complete after user verification.
* Removed stale tracker references to separate UI tokens and project skills, following `AGENTS.md`.
* Recorded runtime limitations and the working verification environment.
* Implemented M2 image I/O and preview; passed 63 automated checks.
* Added dependency setup and manual verification instructions to README.md.
* Replaced the resize pause with periodic updates after user feedback.
* Marked M2 complete after user verification; user will push the commit manually.

## Last Updated

2026-09-15
