"""Build the operation controls."""

from tkinter import ttk


def create_controls(parent):
    parent.columnconfigure(0, weight=1)
    ttk.Label(parent, text="Operation").grid(row=0, column=0, sticky="w")
    ttk.Combobox(parent, state="disabled", width=22).grid(
        row=1, column=0, sticky="ew", pady=(4, 16)
    )
    ttk.Label(parent, text="Parameters").grid(row=2, column=0, sticky="w")
    ttk.Label(parent, text="No operation selected.").grid(
        row=3, column=0, sticky="w", pady=(4, 16)
    )
    ttk.Button(parent, text="Apply", state="disabled").grid(
        row=4, column=0, sticky="ew", pady=(0, 8)
    )
    ttk.Button(parent, text="Reset", state="disabled").grid(
        row=5, column=0, sticky="ew"
    )
