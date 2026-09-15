"""Build the menus, control panel, and image preview area."""

import tkinter as tk
from tkinter import ttk

from gui.controls import OPERATIONS


def create_layout(root, on_exit, on_open, on_save, on_select, on_reset):
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=False)
    file_menu.add_command(label="Open...", command=on_open)
    file_menu.add_command(label="Save As...", command=on_save)
    file_menu.add_command(label="Access Live Webcam", state="disabled")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_exit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    tools_menu = tk.Menu(menu_bar, tearoff=False)
    for operation in OPERATIONS:
        tools_menu.add_command(label=operation, command=lambda name=operation: on_select(name))
    tools_menu.add_separator()
    tools_menu.add_command(label="Reset", command=on_reset)
    menu_bar.add_cascade(label="Tools", menu=tools_menu)
    root.configure(menu=menu_bar)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    content = ttk.Frame(root, padding=12)
    content.grid(row=0, column=0, sticky="nsew")
    content.rowconfigure(0, weight=1)
    content.columnconfigure(1, weight=1)

    controls = ttk.LabelFrame(content, text="Controls", padding=12)
    controls.grid(row=0, column=0, sticky="ns", padx=(0, 12))

    preview = ttk.LabelFrame(content, text="Image Preview", padding=12)
    preview.grid(row=0, column=1, sticky="nsew")
    preview.rowconfigure(0, weight=1)
    preview.columnconfigure(0, weight=1)
    canvas = tk.Canvas(
        preview, background="#FFFFFF", highlightthickness=0, width=1, height=1
    )
    canvas.grid(row=0, column=0, sticky="nsew")
    return canvas, controls


def create_histogram_window(root):
    window = tk.Toplevel(root)
    window.title("Histogram — Displayed Image")
    window.geometry("600x350")
    window.minsize(400, 250)
    canvas = tk.Canvas(window, background="white", highlightthickness=0)
    canvas.histogram_resize_callback = None
    canvas.pack(fill="both", expand=True)
    return canvas


def display_histogram(canvas, counts):
    """Draw already-computed counts; image processing stays outside the GUI."""
    def draw(event=None):
        canvas.delete("all")
        width, height = max(400, canvas.winfo_width()), max(250, canvas.winfo_height())
        left, top, right, bottom = 65, 40, width - 20, height - 45
        peak = max(1, float(counts.max()))
        canvas.create_text(width / 2, 18, text="Grayscale intensity histogram")
        canvas.create_text(10, top - 10, text="Pixels", anchor="w")
        canvas.create_text(left - 6, top + 6, text=f"{peak:g}", anchor="e")
        canvas.create_text(left - 6, bottom, text="0", anchor="e")
        bin_width = (right - left) / 256
        for index, count in enumerate(counts):
            x = left + index * bin_width
            y = bottom - (float(count) / peak) * (bottom - top)
            canvas.create_rectangle(x, y, x + bin_width, bottom, fill="#2563EB", outline="")
        canvas.create_line(left, top, left, bottom, right, bottom)
        for level in (0, 64, 128, 192, 255):
            x = left + level / 255 * (right - left)
            canvas.create_text(x, bottom + 12, text=str(level))
        canvas.create_text(width / 2, height - 12, text="Intensity (0 = black, 255 = white)")

    # Remove the old Tcl callback as well as its binding when counts change.
    if canvas.histogram_resize_callback is not None:
        canvas.unbind("<Configure>", canvas.histogram_resize_callback)
    canvas.histogram_resize_callback = canvas.bind("<Configure>", draw)
    draw()
