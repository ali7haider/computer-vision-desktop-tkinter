"""Coordinate image state, file actions, preview, and application lifecycle."""

import tkinter as tk
from tkinter import filedialog, messagebox

import cv2

from core.file_handler import load_image, save_image
from gui.layout import create_layout


IMAGE_FILE_TYPES = [
    ("PNG image", "*.png"),
    ("JPEG image", "*.jpg *.jpeg"),
    ("BMP image", "*.bmp"),
]


class ComputerVisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Computer Vision Tool")
        self.root.geometry("1000x650")
        self.root.minsize(700, 450)
        self.current_image = None
        self.display_image = None
        self.preview_photo = None
        self.resize_job = None
        self.preview = create_layout(
            self.root, self.close, self.open_image, self.save_image
        )
        self.preview.bind("<Configure>", self.schedule_preview)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def open_image(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Open Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
            + IMAGE_FILE_TYPES + [("All files", "*")],
        )
        if not path:
            return
        try:
            image = load_image(path)
        except (OSError, ValueError, cv2.error):
            messagebox.showerror(
                "Open Failed",
                "Could not open the image. Choose a valid, readable JPG, PNG, or BMP file.",
                parent=self.root,
            )
            return
        # Preserve the loaded original separately from the result to display/save.
        self.current_image = image
        self.display_image = image.copy()
        self.refresh_preview()

    def save_image(self):
        if self.display_image is None:
            messagebox.showwarning(
                "No Image", "Please open an image before saving.", parent=self.root
            )
            return
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save Image As",
            defaultextension=".png",
            filetypes=IMAGE_FILE_TYPES,
        )
        if not path:
            return
        try:
            save_image(path, self.display_image)
        except (OSError, ValueError, cv2.error):
            messagebox.showerror(
                "Save Failed",
                "Could not save the image. Choose a JPG, PNG, or BMP filename "
                "in a folder where you have permission to save.",
                parent=self.root,
            )

    def schedule_preview(self, event):
        # Keep one scheduled update so continuous resizing still refreshes.
        if self.resize_job is None:
            self.resize_job = self.root.after(40, self.refresh_preview)

    def refresh_preview(self):
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
            self.resize_job = None
        width = max(1, self.preview.winfo_width())
        height = max(1, self.preview.winfo_height())
        self.preview.delete("all")
        if self.display_image is None:
            self.preview.create_text(
                width / 2, height / 2, text="Open an image to begin.",
                fill="#64748B", width=width,
            )
            return

        image_height, image_width = self.display_image.shape[:2]
        scale = min(width / image_width, height / image_height, 1.0)
        size = (max(1, int(image_width * scale)), max(1, int(image_height * scale)))
        preview_image = cv2.resize(self.display_image, size, interpolation=cv2.INTER_AREA)
        color_code = cv2.COLOR_GRAY2RGB if preview_image.ndim == 2 else cv2.COLOR_BGR2RGB
        rgb_image = cv2.cvtColor(preview_image, color_code)
        # Tkinter reads PPM directly; no extra image-display dependency is needed.
        ppm = f"P6\n{size[0]} {size[1]}\n255\n".encode("ascii") + rgb_image.tobytes()
        self.preview_photo = tk.PhotoImage(master=self.root, data=ppm, format="PPM")
        self.preview.create_image(width / 2, height / 2, image=self.preview_photo)

    def close(self):
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
            self.resize_job = None
        self.root.destroy()
