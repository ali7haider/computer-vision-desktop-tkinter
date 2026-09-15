# AGENTS.md

This file defines how AI coding agents should work on the **Interactive Computer Vision Tool with GUI**.

This is a small academic project.

The goal is to create a solution that is:

* Correct
* Stable
* Simple
* Easy to understand
* Easy to explain
* Compliant with the assignment requirements

The most important implementation rule is:

> **Expected user actions and invalid input must not crash the application.**

---

# 1. Read Before Working

Before making implementation changes, read:

1. `CV instructions.pdf`
2. `context/project-overview.md`
3. `context/architecture.md`
4. `context/code-standards.md`
5. `context/planning/build-plan.md`
6. `context/planning/progress-tracker.md`

For GUI-related work, also read:

7. `context/ui/ui-rules.md`

Do not assume previous chat history is the source of truth.

Use the assignment instructions, repository context files, and current code.

---

# 2. Project Context

The project context is intentionally small.

```text
context/
├── project-overview.md
├── architecture.md
├── code-standards.md
├── ui/
│   └── ui-rules.md
└── planning/
    ├── build-plan.md
    └── progress-tracker.md
```

Do not create additional context files unless they solve a real project need.

We intentionally do not maintain:

```text
decision-log.md
library-docs.md
ui-registry.md
ui-tokens.md
session files
templates
skills
```

---

# 3. Source of Truth

When instructions conflict, use this priority:

```text
Assignment Requirements / Current User Instruction
                    ↓
                AGENTS.md
                    ↓
         project-overview.md
                    ↓
            architecture.md
                    ↓
          code-standards.md
                    ↓
              ui-rules.md
                    ↓
             build-plan.md
                    ↓
         progress-tracker.md
                    ↓
             Existing Code
```

Assignment requirements always take priority over implementation preferences.

Do not silently change established project rules.

---

# 4. Project Structure

Follow the agreed structure:

```text
ComputerVisionApp/
│
├── AGENTS.md
├── README.md
├── CV instructions.pdf
│
├── context/
│   ├── project-overview.md
│   ├── architecture.md
│   ├── code-standards.md
│   ├── ui/
│   │   └── ui-rules.md
│   └── planning/
│       ├── build-plan.md
│       └── progress-tracker.md
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
└── utils/
    ├── __init__.py
    └── validators.py
```

Source folders/files may be created as their milestone begins.

Do not introduce additional folders or architectural layers without a clear need.

---

# 5. Responsibilities

Keep responsibilities clear.

```text
main.py
→ Start the application

app.py
→ Coordinate application state and functionality

gui/
→ Tkinter layout and controls

core/file_handler.py
→ Open and save images

core/webcam.py
→ Webcam lifecycle and frames

processing/
→ Computer vision algorithms

utils/validators.py
→ Parameter/input validation
```

Do not place computer-vision algorithms directly inside GUI layout code.

---

# 6. Development Workflow

Before implementing a feature:

```text
Understand Requirement
        ↓
Read Relevant Context
        ↓
Inspect Existing Code
        ↓
Implement Smallest Correct Solution
        ↓
Run Application
        ↓
Test Normal Case
        ↓
Test Invalid Cases
        ↓
Fix Problems
        ↓
Verify Stability
        ↓
Update Progress
```

Do not immediately generate large amounts of code.

Understand the existing implementation first.

---

# 7. Keep the Project Simple

This is an academic project, not production software.

Do not introduce:

* Enterprise architecture
* Dependency injection
* Plugin systems
* Complex design patterns
* Deep class hierarchies
* Complex configuration systems
* Backend services
* Databases
* APIs
* Cloud infrastructure
* Complex logging systems
* Unnecessary dependencies

Prefer straightforward implementations.

Example:

```python
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

Every major part of the implementation should be understandable and explainable during evaluation.

---

# 8. No-Crash Rule

Application stability is a major requirement.

Expected user mistakes must not terminate the application.

Always consider:

* What if no image is loaded?
* What if an input is empty?
* What if numeric input contains text?
* What if a value is negative?
* What if a kernel size is invalid?
* What if the webcam is unavailable?
* What if reading a webcam frame fails?
* What if the user cancels a dialog?
* What if an image cannot be opened?
* What if an image cannot be saved?

Expected behavior:

```text
Invalid Situation
       ↓
Detect
       ↓
Show Clear Message
       ↓
Return Safely
       ↓
Application Continues
```

Never knowingly leave an obvious crash path.

Do not hide programming bugs with broad exception handling. Handle expected failure cases deliberately.

---

# 9. Validation

Never pass unchecked user textbox values directly into OpenCV.

Validate first.

Examples:

```text
Kernel Size
→ integer
→ positive
→ odd
→ acceptable range

Threshold
→ numeric
→ acceptable range

Sigma
→ numeric
→ valid range

Aperture Size
→ OpenCV-supported value
```

Put reusable validation in:

```text
utils/validators.py
```

Do not over-generalize validation helpers.

---

# 10. Image Processing

Processing algorithms belong in:

```text
processing/
```

Functions should normally:

1. Receive an image.
2. Receive required parameters.
3. Perform one operation.
4. Return the processed image/result.

Example:

```python
def gaussian_blur(image, kernel_size, sigma):
    ...
    return processed_image
```

Processing functions should remain independent from Tkinter where practical.

Use the existing categories:

```text
color.py
statistics.py
filters.py
edges.py
segmentation.py
```

Do not create a separate class or file for every individual operation.

---

# 11. GUI Rules

For GUI work, follow:

```text
context/ui/ui-rules.md
```

The GUI should be:

* Simple
* Clear
* Consistent
* Easy to demonstrate

General layout:

```text
┌──────────────────────────────────────────┐
│ File        Tools                        │
├─────────────┬────────────────────────────┤
│             │                            │
│ Controls    │       Image Preview        │
│             │                            │
│ Parameters  │                            │
│             │                            │
│ Apply       │                            │
│ Reset       │                            │
│             │                            │
└─────────────┴────────────────────────────┘
```

Do not add visual complexity unless it improves usability.

---

# 12. Webcam Rules

Webcam functionality belongs primarily in:

```text
core/webcam.py
```

Required flow:

```text
Start Webcam
     ↓
Verify Camera
     ↓
Read Frames
     ↓
Display
     ↓
Take Snapshot
     ↓
Stop Webcam
     ↓
Release Camera
     ↓
Use Snapshot as Current Image
```

Always release webcam resources when:

* Webcam is stopped
* Snapshot is taken
* Webcam fails
* Application exits

Webcam failure must not crash the application.

---

# 13. Scope Control

Implement only what the current milestone or task requires.

If the task is:

```text
Implement Median Filter
```

do not also:

* Redesign the GUI
* Refactor webcam code
* Add unrelated processing operations
* Introduce unnecessary libraries
* Restructure the project

Follow:

```text
Requested Change
      ↓
Necessary Supporting Changes
      ↓
STOP
```

Do not modify unrelated code simply because it is nearby.

---

# 14. Build Plan

Development follows:

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

Follow:

```text
context/planning/build-plan.md
```

Do not jump ahead unless explicitly requested.

---

# 15. Testing

A feature is not complete simply because its code exists.

For each relevant feature, test:

## Normal Case

Does it work with valid input?

## No Image

What happens if it is used before loading/capturing an image?

## Invalid Parameters

Where applicable, test:

* Empty input
* Text instead of numbers
* Zero
* Negative values
* Invalid even kernel
* Too-small values
* Too-large values

## Repeated Usage

Can the feature be used multiple times without breaking application state?

## Integration

Does the application remain usable afterward?

---

# 16. Verification

Do not claim:

```text
Works correctly
```

or:

```text
No crashes
```

unless the relevant behavior was actually tested.

Report exactly what was verified.

If something could not be tested, say so.

---

# 17. Structural Change Rule

The architecture and build plan already define normal development.

Before making a significant structural change:

1. Read `architecture.md`.
2. Inspect the current implementation.
3. Identify why the existing structure is insufficient.
4. Prefer the smallest change possible.
5. Consider affected modules.
6. Verify the change does not introduce unnecessary complexity.

A significant change includes:

* Changing the agreed folder structure
* Changing major module responsibilities
* Introducing a major dependency
* Changing the main image-processing flow
* Changing application-wide state handling

Normal planned feature implementation does not require architectural redesign.

---

# 18. Review Rule

Perform a focused review:

* After completing a milestone
* After risky integration changes
* Before the final demo
* Before final submission

Review should focus on:

* Assignment compliance
* Correct functionality
* Invalid input handling
* Crash paths
* Webcam/resource cleanup
* Code simplicity
* Architecture compliance
* GUI usability

For this project, stability and correctness are more important than stylistic perfection.

---

# 19. Recovery Rule

If a meaningful fix does not solve a problem, do not keep stacking patches.

Use:

```text
Problem
   ↓
Investigate
   ↓
Attempt Minimal Fix
   ↓
Still Broken?
   ↓
Stop Adding Patches
   ↓
Find Root Cause
   ↓
Implement Correct Fix
   ↓
Verify
```

This is especially important for:

* Tkinter state problems
* Webcam lifecycle problems
* Image conversion/display problems
* OpenCV parameter errors
* Processing state problems

Fix the cause rather than hiding the symptom.

---

# 20. Progress Tracking

Use:

```text
context/planning/progress-tracker.md
```

It should answer:

* What milestone are we on?
* What is currently being implemented?
* What is complete?
* What remains?
* Is anything blocked?

Update it when:

* A meaningful feature is completed
* A milestone is completed
* Work becomes blocked
* The next task changes

Do not update it for every tiny code edit.

---

# 21. Documentation Updates

Only update context when the underlying information changes.

```text
Project scope changed
→ project-overview.md

Architecture/responsibility changed
→ architecture.md

Coding convention changed
→ code-standards.md

GUI rule changed
→ ui-rules.md

Development sequence changed
→ build-plan.md

Feature/milestone status changed
→ progress-tracker.md
```

Do not create documentation for documentation's sake.

---

# 22. Dependencies

Keep dependencies minimal.

Expected dependencies are primarily:

```text
Python
OpenCV
NumPy
Tkinter
```

Before adding another dependency:

1. Check whether OpenCV, Tkinter, NumPy, or Python already solves the problem.
2. Determine whether the dependency is genuinely necessary.
3. Avoid adding dependencies merely to save a few lines of code.

---

# 23. Comments

Comment code when the reason is not obvious.

Useful:

```python
# Gaussian kernel dimensions must be positive odd numbers.
```

Unnecessary:

```python
# Set kernel size
kernel_size = 5
```

Comments should help the student understand and explain the implementation.

---

# 24. Forbidden Patterns

Do not introduce:

* Giant single-file implementations
* Giant functions
* Unnecessary classes
* Complex inheritance
* Duplicate processing logic
* Circular imports
* Wildcard imports
* Hardcoded local file paths
* Unchecked user parameters
* Empty `except:` blocks
* Silent failures
* Processing algorithms inside GUI layout code
* Unnecessary external libraries
* Unnecessary folders
* Production architecture
* Large unrelated refactors

Most importantly:

> Do not trade simplicity and stability for architectural sophistication.

---

# 25. Definition of Done

A feature is complete when:

* Required behavior is implemented.
* The application still launches.
* Valid input works.
* Relevant invalid input is handled.
* No known expected user action crashes the application.
* Code follows agreed responsibility boundaries.
* Code is understandable.
* Relevant verification has been performed.
* Progress tracker is updated when appropriate.

A milestone is complete only when all planned features meet these conditions.

---

# 26. Final Review

Before the final demo/submission, test the complete workflow:

```text
Launch
 ↓
Open Image
 ↓
Run Every Operation
 ↓
Adjust Parameters
 ↓
Try Invalid Parameters
 ↓
Save Result
 ↓
Start Webcam
 ↓
Take Snapshot
 ↓
Process Snapshot
 ↓
Save Snapshot Result
 ↓
Start/Stop Webcam Again
 ↓
Exit Cleanly
```

Also intentionally test incorrect usage.

The expected result should always be:

```text
Operation succeeds
```

or:

```text
Clear feedback + application continues
```

Never an avoidable application crash.

---

# 27. Final Principle

When deciding how to implement something:

```text
Does it satisfy the assignment?
            ↓
Is it correct?
            ↓
Can expected usage crash it?
            ↓
Is it simple?
            ↓
Can the student explain it?
            ↓
Does it follow the project structure?
```

If a simpler implementation satisfies all of these requirements, prefer it.

**This project rewards correct, stable, understandable functionality — not unnecessary engineering complexity.**
