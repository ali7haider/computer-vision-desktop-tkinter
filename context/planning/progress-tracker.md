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

**M5 — Edge Detection: complete.**

**M6 — Segmentation: complete.**

**M7 — Webcam + Snapshot: complete; covered by user-confirmed M8 integration verification.**

**M8 — Integration + Stability: complete; user verification confirmed.**

**M9 — Documentation: complete for the agreed editable-DOCX scope.**

## Current Task

M1–M9 remain complete for the agreed scope. User requested optional Windows EXE
packaging and macOS packaging on 2026-09-17. Build configuration and beginner
build/install instructions are added; packaging verification is recorded below.
Packaging documentation is prepared for commit. Manual packaged-app verification
remains outstanding; no additional runtime verification is inferred from this
documentation update.

### Optional Desktop Packaging — 2026-09-17

* Added `computer_vision.spec`: Windows single-file, windowed EXE and macOS app
  bundle with a camera usage description. Existing application source is unchanged.
* Added build-only dependencies in `requirements-build.txt` and ignored generated
  build/output/environment folders. README explains platform-specific builds,
  portable Windows installation, macOS Applications installation, and verification.
* Expanded README source installation for a fresh Windows or macOS computer:
  install Python, recreate local environments, install requirements, check Tkinter,
  launch without activation, and troubleshoot setup. These documentation updates
  do not represent a new Windows runtime test.
* Checked both spec branches with mocked PyInstaller constructors, including
  Windows embedded dependencies and macOS camera metadata. These checks do not
  constitute a Windows build or runtime test.
* macOS Intel build succeeded with Python 3.13.13, PyInstaller 6.22.3, OpenCV
  4.12.0.88, and NumPy 2.2.6. Output: `dist/ComputerVisionTool.app` (about 252 MiB).
  Separate build environment passes `pip check`. Bundle camera metadata and
  `codesign --verify --deep --strict` passed (local ad-hoc signature, not Developer
  ID signing or notarization).
* Packaged app remained running for eight seconds when launched outside the source
  folder, with no captured startup errors. The check terminated the process;
  interactive GUI actions, normal GUI exit, and physical webcam were not tested.
  Windows and macOS spec branches passed configuration checks; whitespace checks
  passed. User verification of the packaged workflow remains pending.
* Windows build/runtime, target-machine compatibility, and packaged webcam tests
  require verification on the corresponding machines before distribution.

## Completed

### Code Documentation

* Added `context/code-documentation.md` explaining the committed M1/M2 code,
  state, callback flow, preview conversion, resizing, file I/O, and error handling.
* Updated `AGENTS.md` to require code documentation after user verification,
  before implementation commits.
* Rewrote the guide for beginners and added an explanation of the packaging recipe,
  build dependencies, output files, and platform limitations. Runtime verification
  limits remain explicit.

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

## Milestone Details

### M9 — Complete for Agreed Scope

User requested completion through M9 on 2026-09-16. The delivered scope is an
editable DOCX with screenshot spaces/captions; PDF export and video production
were not part of this task.

* Created `Computer_Vision_Project_Report.docx`, organized with five page breaks
  for a six-page report layout: overview, color/statistics, filters/edges,
  segmentation, parameters, and implementation/webcam/verification.
* Includes all thirteen operation subsections, a sixteen-row parameter reference
  with control types/ranges/defaults/effects, architecture, validation, camera
  cleanup, save behavior, setup, and honest verification limitations.
* Includes five blank screenshot areas with captions and editable student fields.
  No screenshots were captured or inserted, as requested.
* Checked DOCX reopening, page-break count, table rows, and placeholder captions.
  Visual rendering/pagination has not been verified in Word or a PDF renderer;
  user should check the final 3–6 page PDF after inserting screenshots.
* User will edit and export the PDF. No video was produced. The assignment still
  requests a 2–4 minute video and first-page link; final assignment packaging is
  separate from completion of the agreed M9 work.


### M8 — Integration + Stability: Complete

User confirmed M8 verification on 2026-09-16. Individual manual test results were
not recorded; the confirmation covers the integration milestone as a whole.

* Reviewed the restored build plan, assignment coverage, processing boundaries,
  validation, callback lifecycle, file handling, and webcam cleanup. All thirteen
  planned operations are present across the five required categories.
* All 914 existing checks passed: 63 M2, 147 M3, 111 M4, 165 M5, 354 M6, and 74 M7.
  Real Tk windows were used; dialogs and cameras were simulated.
* Reproduced a Save As timing bug: a pending slider callback could change the image
  saved while the native dialog was open. Saving now takes a copy of the displayed
  result before opening the dialog, preserving the pixels selected for saving.
* 470 new end-to-end checks passed after the fix: pending-slider save reproduction,
  all thirteen operations on normal/tiny/thin images, original preservation,
  repeated Apply, Reset, PNG/BMP exact pixel saving, JPEG dimensions, and callback
  error detection. The 63 M2 and 74 M7 checks were rerun after the fix.
* All 16 Python files passed syntax parsing; whitespace checks passed.
* Added a complete manual integration checklist to README. Native Save As clipping
  remains unresolved; the reverted workaround has not been reintroduced.
* User verification is confirmed and code documentation now explains the Save As
  timing fix. Camera hardware was not independently tested by the agent. No new
  dependencies or architectural layers were added.


### M7 — Webcam + Snapshot: Complete

Included in the user-confirmed M8 integration verification; detailed hardware
check results were not individually recorded.

* Added `core/webcam.py` to own the default camera, check availability/read results,
  and release the handle on stop and expected capture failures.
* Enabled File → Access Live Webcam. Added Take Snapshot and Stop Webcam below
  the preview, visible only during capture. Both disappear after snapshot, stop,
  failure, or successful image open; the empty button row is also hidden.
* Live frames use one pending Tkinter callback, scheduled 30 ms after each frame.
  Preview retains proportions and uses a separate latest frame; static image state
  remains intact until a snapshot or successful image open replaces it.
* Snapshot copies the full-resolution frame, releases the camera, clears operation
  selection, and becomes the original for all processing and saving operations.
* Stop/failure restores the prior static result, parameters, and label. Processing
  and saving are guarded during capture; an existing histogram closes on start.
  Successful image opens stop capture; cancelled/failed opens preserve live mode.
* Exit cancels frame/processing/preview callbacks and releases the camera.
* Added a direct Save As… button below Reset, using the existing save callback.
  Button invocation verified for no image, live capture, and saving a processed
  snapshot. M6 checks confirmed controls still fit the minimum window size.
* 74 simulated-camera checks passed with real Tk windows: button visibility,
  unavailable camera,
  failed reads and OpenCV exceptions, no-frame snapshot, repeated start/stop,
  single camera handle, live updates, controls/guards, static state restoration,
  snapshot independence, processing and full-resolution PNG saving, Open behavior,
  minimum-window layout, and shutdown with pending callbacks.
* 354 M6, 144 M3, and 63 M2 regression checks passed. All 16 Python files passed syntax
  parsing; whitespace checks passed. No dependencies were added.
* Actual camera hardware, OS permission prompts, driver responsiveness, and physical
  camera release have not been tested by the agent. README includes manual steps.
  Code documentation now covers camera ownership, scheduling, snapshot/stop flow,
  state preservation, button visibility, guards, and the direct Save As button.

### M6 — Segmentation: Complete

User confirmed M6 works on 2026-09-16. Individual manual test results were not recorded.

* Added global thresholding, adaptive thresholding, and contour detection in
  `processing/segmentation.py`; thirteen operations are now available.
* Global thresholding uses a live 0–255 slider (default 127) to produce a binary
  grayscale mask. Contours use the same threshold internally and draw external
  boundaries in green on a color copy of the original, with a live slider.
* Adaptive thresholding exposes block size (odd 3–31, default 11), constant C
  (finite −50–50, default 2), and Mean/Gaussian choice (default Gaussian).
  Edits run on Apply. Validation names the block-size field correctly.
* Applied-result labels now support text-valued parameters such as Method.
  Existing original-image processing, Reset, error preservation, histogram,
  preview, and saving behavior are retained.
* 354 M6 algorithm/GUI checks passed: exact global thresholds, independent local
  3×3 adaptive calculations for both methods, tiny/constant images, boundaries,
  invalid values, contour position and external-only behavior, unchanged originals,
  no-image handling, live threshold updates, method labels, repeated Apply, Reset,
  simulated OpenCV failures, histogram integration, full-resolution PNG saving,
  operation switching, new-image loading, and shutdown with pending processing.
* Controls fit real Tk windows at 700×450, 1000×650, and 1200×800. GUI controls were
  driven programmatically; file dialogs and error messages were simulated.
* All 165 M5, 111 M4, and 144 M3 regression checks passed. All 15 Python files
  passed syntax parsing and whitespace checks passed. No dependencies were added.
* README contains M6 behavior, range rationale, limitations, and manual steps.
  Code documentation now covers verified M6 algorithms, controls, callback flow,
  image representations, validation, label formatting, and range choices.

### M5 — Edge Detection: Complete

User confirmed M5 works on 2026-09-16. Individual manual test results were not recorded.

* Added Sobel and Canny in `processing/edges.py`; ten operations are available.
* Sobel uses signed horizontal/vertical derivatives and thresholds their magnitude
  strictly above `mean_ratio × mean magnitude`, producing a binary uint8 image.
  Kernel choices are 3/5/7; mean ratio accepts finite values 0–10 (default 1).
* Canny exposes threshold 1/2 textboxes (0–255, defaults 100/200) and an aperture
  dropdown (3/5/7, default 3). Threshold 1 must not exceed threshold 2.
* Selection applies defaults. Edited controls run on Apply. Reset restores the
  original/defaults while retaining the operation. Invalid input preserves the
  previous result and applied-result label. Parameters are disabled without an image.
* 165 M5 checks passed: independent 3×3 Sobel kernel calculation, both edge
  polarities/directions, ratio behavior, Canny edge localization, constant/tiny
  images, supported sizes, boundaries, invalid/nonfinite inputs, no-image handling,
  repeated Apply, Reset, simulated OpenCV errors, histogram integration,
  full-resolution PNG saving, new-image loading, and callback cleanup.
* Real Tk controls fit at 700×450, 1000×650, and 1200×800. GUI actions were driven
  programmatically; file dialogs and error messages were simulated.
* All 111 M4 and 139 M3 regression checks passed. All 14 Python files passed syntax
  parsing; whitespace checks passed. No dependencies were added.
* README now includes parameter choices, algorithm behavior, and manual steps.
  Code documentation now covers the verified M5 controls, execution flow, edge
  algorithms, validation, image representation, and parameter-range rationale.

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

* User reported initial clipping of the native macOS Save As dialog. The proposed
  standalone-dialog change was reverted by the user; the parented dialog remains.
  This visual issue is unresolved and excluded from the M7 fix claims.

* The default pyenv Python 3.11.7 lacks `_tkinter`.
* System Python 3.9.6 imports Tk but aborts on GUI launch with a macOS version compatibility error.
* `.venv` uses the working framework Python 3.13.13 and has OpenCV/NumPy installed.
  Run the application from the project directory:

```bash
.venv/bin/python main.py
```

The application contains no machine-specific paths. README.md includes environment setup
instructions. OpenCV is constrained to version 4.x to use compatible prebuilt packages.

## Review / Submission Follow-ups

* No active milestone implementation remains through M9 in the agreed scope.
* User will fill report details/screenshots, check pagination, and export PDF.
* Video remains an assignment deliverable but was excluded from this task.
* Native Save dialog clipping remains a known issue for review.

## Next Steps

1. Build the EXE on Windows using README and manually verify the packaged workflow.
2. Manually verify the generated macOS app, including camera permissions and exit.
3. Record manual verification results when available and update documentation if
   those results change the described behavior or limitations.
4. Share for review and collect feedback.

## Recent Changes

* Added optional Windows/macOS packaging and beginner build/install instructions;
  built and launch-smoke-checked the macOS app. Windows runtime verification remains.

* Marked M1–M9 complete for the user-agreed scope and moved to review handoff.

* Prepared the editable M9 DOCX report with screenshot spaces/captions; PDF export
  is left to the user and video production is excluded from this task.

* Marked M8 complete after user verification and documented the Save As timing fix.

* Completed M8 automated integration review and fixed Save As pixels changing
  during a pending slider callback. Added final manual verification steps.

* Documented current M7 code at the user’s request, including hidden webcam
  buttons and direct Save As. Recorded the reverted dialog workaround as unresolved.

* Implemented M7 webcam lifecycle, live preview, snapshot, and stop controls;
  simulated-camera checks passed, with physical-camera verification pending.

* Marked M6 complete after user confirmation and updated code documentation.

* Implemented and automatically verified M6 segmentation operations and controls.

* Marked M5 complete after user confirmation and updated code documentation.

* Implemented and automatically verified M5 Sobel/Canny edge detection.
* Restored the committed build plan at the user's request after finding an
  uncommitted empty template in its place.

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

2026-09-17
