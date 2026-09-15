"""Build the menus, control panel, and image preview area."""

import tkinter as tk
from tkinter import ttk

from gui.controls import create_controls


def create_layout(root, on_exit):
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=False)
    file_menu.add_command(label="Open...", state="disabled")
    file_menu.add_command(label="Save As...", state="disabled")
    file_menu.add_command(label="Access Live Webcam", state="disabled")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=on_exit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    tools_menu = tk.Menu(menu_bar, tearoff=False)
    tools_menu.add_command(label="Processing Operations", state="disabled")
    tools_menu.add_command(label="Reset", state="disabled")
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
    create_controls(controls)

    preview = ttk.LabelFrame(content, text="Image Preview", padding=12)
    preview.grid(row=0, column=1, sticky="nsew")
    preview.rowconfigure(0, weight=1)
    preview.columnconfigure(0, weight=1)
    ttk.Label(preview, text="No image loaded.", anchor="center").grid(
        row=0, column=0, sticky="nsew"
    )
