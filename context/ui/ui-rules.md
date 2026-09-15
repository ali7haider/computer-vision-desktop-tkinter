# UI Rules

This file defines the basic visual and usability rules for the application.

The GUI should remain:

**Simple → Clear → Consistent → Easy to Use → Easy to Demonstrate**

This is an academic Tkinter application. Functionality and clarity are more important than advanced visual design.

---

## Design Principles

* Keep the interface simple and clean.
* Functionality comes before decoration.
* The image preview should be the main focus.
* Related controls should be grouped together.
* Similar controls should look and behave consistently.
* Avoid unnecessary visual complexity.
* The user should easily understand what to do next.

---

## Layout

Use a simple desktop layout:

```text
┌──────────────────────────────────────────────────┐
│ File        Tools                                │
├───────────────┬──────────────────────────────────┤
│               │                                  │
│   Controls    │                                  │
│               │          Image Preview           │
│   Operation   │                                  │
│   Parameters  │                                  │
│               │                                  │
│   Apply       │                                  │
│   Reset       │                                  │
│               │                                  │
└───────────────┴──────────────────────────────────┘
```

The image preview should receive most of the available space.

The controls area should contain only controls relevant to the current operation where practical.

Do not overcrowd the interface.

---

## Colors

Use a small, consistent palette.

```text
Primary:        #2563EB
Secondary:      #64748B

Background:     #F1F5F9
Surface:        #FFFFFF

Primary Text:   #1E293B
Secondary Text: #64748B

Border:         #CBD5E1

Success:        #16A34A
Warning:        #D97706
Error:          #DC2626
```

Do not introduce random colors for individual controls.

Default Tkinter colors may be used where custom styling provides no real benefit.

---

## Spacing

Use simple, consistent spacing.

```text
Small:    4 px
Medium:   8 px
Large:   12 px
Section: 16 px
```

Example:

```python
widget.pack(padx=8, pady=8)
```

Related controls should be closer together than separate sections.

Exact spacing may vary slightly when needed for the layout.

---

## Typography

Prefer standard system fonts.

Recommended:

```text
Font: Arial or Tkinter system default

Application Title: 18
Section Heading:   14
Normal Text:       11
Small Text:        10
```

Use mainly:

```text
Normal
Bold
```

Do not add custom font dependencies.

---

## Icons

Icons are optional.

Prefer clear text labels such as:

```text
Open Image
Save As
Apply
Reset
Take Snapshot
```

Do not add an icon library purely for decoration.

---

## Buttons

Buttons should have clear action-oriented labels.

Examples:

```text
Apply
Reset
Take Snapshot
```

Important actions should be easy to find.

Use consistent button sizing where practical.

Avoid creating buttons for actions that are better represented by menus or parameter controls.

---

## Inputs

Choose controls according to the parameter.

### Sliders

Prefer sliders for values that benefit from interactive adjustment.

Examples:

* Brightness
* Contrast
* RGB values
* Thresholds

### Textboxes

Use numeric textboxes when exact input is useful.

Examples:

* Kernel size
* Sigma
* Block size

### Dropdowns

Use dropdowns when the user must choose from a small fixed set of options.

Examples:

```text
Adaptive Method
Sobel Direction
```

Do not use free-text input when only a few valid choices exist.

---

## Forms

No complex form system is required.

A processing operation should generally present:

```text
Operation Name

Parameter 1    [ Control ]
Parameter 2    [ Control ]

[ Apply ]
```

Only show parameters that are relevant to the selected operation where practical.

---

## Validation

Invalid input must never cause an avoidable application crash.

Examples of values that require validation:

* Kernel sizes
* Thresholds
* Sigma values
* Aperture sizes
* Block sizes
* Numeric textbox values

Example message:

```text
Kernel size must be a positive odd integer.
```

Validation messages should be:

* Short
* Clear
* Specific
* Helpful

Where appropriate, a safe default may be used instead.

---

## Navigation

Use the Tkinter menu bar for major application actions.

Example:

```text
File
├── Open...
├── Save As...
├── Access Live Webcam
└── Exit

Tools
├── Processing Operations
└── Reset
```

Keep navigation shallow.

The user should not need to move through multiple windows to perform normal image processing.

---

## Modals / Dialogs

Use standard Tkinter dialogs for:

* Opening files
* Saving files
* Errors
* Warnings
* Important information

Avoid unnecessary custom modal windows.

---

## Drawers

Not required.

Do not implement drawer-style navigation.

---

## Dropdowns

Dropdowns are acceptable for small fixed selections.

Keep option names short and understandable.

---

## Tables

Not required unless a later assignment requirement specifically needs one.

---

## Lists

Use simple lists only when they provide a clear functional benefit.

---

## Cards

No card-based design system is required.

Use simple Tkinter frames to visually group related controls.

---

## Tabs

Avoid tabs unless the number of processing controls becomes difficult to manage on one screen.

Do not introduce tabs purely for visual styling.

---

## Tooltips

Optional.

Use a tooltip only when a parameter or control cannot be understood easily from its label.

Do not add tooltips to every control.

---

## Notifications

Use Tkinter message dialogs for important feedback.

Examples:

```text
Please load an image first.

Could not access the webcam.

Image saved successfully.
```

Do not show a success popup after every normal processing operation.

---

## Loading States

No advanced loading system is required.

Normal image operations should remain simple and responsive.

The GUI should not be intentionally blocked while the webcam is running.

---

## Empty States

When no image is loaded, the preview area may display:

```text
Open an image or access the webcam to begin.
```

The empty state should make the next action obvious.

---

## Error States

When something fails:

```text
Detect Problem
      ↓
Show Clear Message
      ↓
Return Safely
      ↓
Application Continues
```

Do not display unnecessary technical stack traces to the user.

Expected errors must not close the application.

---

## Success States

Success feedback should be used only when useful.

For example:

```text
Image saved successfully.
```

Normal processing operations usually do not need success dialogs because the visible processed image already provides feedback.

---

## Responsive Behavior

This is a desktop Tkinter application.

Web-style responsive breakpoints are not required.

Where practical:

* Image preview should expand with the window.
* Controls should remain accessible.
* Resizing the window should not break the layout.

---

## Accessibility

Keep basic accessibility in mind.

Use:

* Readable text
* Clear labels
* Good contrast
* Reasonably sized buttons
* Understandable error messages

Do not communicate important information using color alone.

---

## Keyboard Interaction

Default Tkinter keyboard behavior is sufficient.

Keyboard shortcuts may be added later if useful, but they are not required.

---

## Focus States

Keep standard Tkinter focus behavior.

Do not intentionally remove useful focus indicators.

---

## Hover / Active States

Default Tkinter behavior is sufficient.

No custom hover system is required.

---

## Animation

Do not add decorative animations.

Continuous updates are allowed when required for functionality, such as:

* Webcam frames
* Slider-driven image updates

---

## Content / Copy

Use short and direct labels.

Prefer:

```text
Open Image
Brightness
Contrast
Kernel Size
Threshold
Apply
Reset
Save As
```

Avoid:

* Long instructions inside the interface
* Highly technical wording
* Unclear abbreviations
* Decorative text

The GUI should be understandable without requiring extensive instructions.

---

## Reuse Rules

Reuse existing GUI patterns.

If one processing operation already uses a standard parameter layout, use the same pattern for similar operations.

Reuse:

* Button styles
* Input layouts
* Parameter groups
* Validation messages
* Dialog behavior
* Section spacing

Do not create a completely different UI style for every operation.

---

## Forbidden Patterns

Avoid:

* Overcrowded screens
* Random colors
* Excessive styling
* Decorative gradients
* Custom shadows
* Complex animations
* Tiny text
* Tiny buttons
* Too many popups
* Deep navigation
* Unnecessary tabs
* Unnecessary custom widgets
* Different styles for similar controls
* Long instructions inside the GUI
* Adding UI libraries without a clear need
* UI complexity that makes the code difficult to understand

---

## Main GUI Flow

The normal user workflow should remain obvious:

```text
Open Image / Webcam
        ↓
Choose Operation
        ↓
Adjust Parameters
        ↓
See Result
        ↓
Save
```

For webcam:

```text
Access Webcam
      ↓
View Live Feed
      ↓
Take Snapshot
      ↓
Process Snapshot
      ↓
Save
```

---

## Main Rule

When adding or changing GUI functionality, ask:

> Can the user easily understand the control, change the required parameter, see the result, and recover safely from invalid input?

If yes, the UI is sufficient.

Do not make the GUI more sophisticated than necessary for the assignment.
