"""Build the operation selector and its relevant parameter controls."""

import tkinter as tk
from tkinter import ttk


OPERATIONS = (
    "Grayscale", "Brightness / Contrast", "RGB Channels",
    "Histogram", "Histogram Equalization",
    "Median Filter", "Gaussian Smoothing", "Sharpening",
)


class OperationControls:
    def __init__(self, parent, on_select, on_apply, on_reset, on_change):
        self.on_change = on_change
        self.image_loaded = False
        self.values = {}
        self.sliders = []
        self.entries = []
        self.operation = tk.StringVar(parent, value="")
        parent.columnconfigure(0, weight=1)
        ttk.Label(parent, text="Operation").grid(row=0, column=0, sticky="w")
        selector = ttk.Combobox(
            parent, textvariable=self.operation, values=OPERATIONS,
            state="readonly", width=26,
        )
        selector.grid(row=1, column=0, sticky="ew", pady=(4, 12))
        selector.bind("<<ComboboxSelected>>", lambda event: on_select(self.operation.get()))
        self.parameters = ttk.Frame(parent)
        self.parameters.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self.parameters.columnconfigure(0, weight=1)
        ttk.Button(parent, text="Apply", command=on_apply).grid(
            row=3, column=0, sticky="ew", pady=(0, 8)
        )
        ttk.Button(parent, text="Reset", command=on_reset).grid(
            row=4, column=0, sticky="ew"
        )
        self.choose("")

    def choose(self, operation):
        self.operation.set(operation)
        for child in self.parameters.winfo_children():
            child.destroy()
        self.values = {}
        self.sliders = []
        self.entries = []
        if operation == "Brightness / Contrast":
            self.add_slider("Brightness", -255, 255, 0, 1)
            self.add_slider("Contrast", 0, 3, 1, 0.05)
        elif operation == "RGB Channels":
            for name in ("Red", "Green", "Blue"):
                self.add_slider(name, 0, 2, 1, 0.05)
        elif operation == "Median Filter":
            self.add_entry("Kernel Size (odd: 3–31)", "kernel_size", "3")
            ttk.Label(self.parameters, text="Edit the value, then click Apply.").grid(sticky="w")
        elif operation == "Gaussian Smoothing":
            self.add_entry("Kernel Size (odd: 3–31)", "kernel_size", "5")
            self.add_entry("Sigma (0–10; 0 = automatic)", "sigma", "0")
            ttk.Label(self.parameters, text="Edit values, then click Apply.").grid(sticky="w")
        else:
            text = {
                "": "Choose an operation to begin.",
                "Grayscale": "Convert to grayscale.",
                "Histogram": "Grayscale intensity counts\nof the displayed image.",
                "Histogram Equalization": "Equalize grayscale intensities.\nThe result is grayscale.",
                "Sharpening": "Emphasize local detail using\na fixed 3×3 sharpening kernel.",
            }[operation]
            ttk.Label(self.parameters, text=text, wraplength=230).grid(sticky="w")

    def add_slider(self, name, minimum, maximum, default, step):
        row = len(self.sliders) * 2
        ttk.Label(self.parameters, text=name).grid(row=row, column=0, sticky="w")
        value = tk.DoubleVar(self.parameters, value=default)
        slider = tk.Scale(
            self.parameters, from_=minimum, to=maximum, resolution=step,
            orient="horizontal", variable=value, length=220,
            highlightthickness=0, state="normal" if self.image_loaded else "disabled",
            command=lambda unused: self.on_change(),
        )
        slider.grid(row=row + 1, column=0, sticky="ew", pady=(0, 8))
        self.values[name.lower()] = value
        self.sliders.append(slider)

    def add_entry(self, label, name, default):
        row = len(self.entries) * 2
        ttk.Label(self.parameters, text=label).grid(row=row, column=0, sticky="w")
        value = tk.StringVar(self.parameters, value=default)
        entry = ttk.Entry(
            self.parameters, textvariable=value,
            state="normal" if self.image_loaded else "disabled",
        )
        entry.grid(row=row + 1, column=0, sticky="ew", pady=(4, 12))
        self.values[name] = value
        self.entries.append(entry)

    def set_image_loaded(self, loaded):
        self.image_loaded = loaded
        for slider in self.sliders:
            slider.configure(state="normal" if loaded else "disabled")
        for entry in self.entries:
            entry.configure(state="normal" if loaded else "disabled")

    def get_parameters(self):
        return {name: value.get() for name, value in self.values.items()}
