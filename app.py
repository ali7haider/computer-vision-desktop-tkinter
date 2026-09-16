"""Coordinate image state, file actions, preview, and application lifecycle."""

import tkinter as tk
from tkinter import filedialog, messagebox

import cv2

from core.file_handler import load_image, save_image
from gui.controls import OperationControls
from gui.layout import create_layout, create_histogram_window, display_histogram
from processing.color import grayscale, brightness_contrast, rgb_channels
from processing.statistics import compute_histogram, equalize_histogram
from processing.filters import median_filter, gaussian_smoothing, sharpen


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
        self.processing_job = None
        self.histogram_canvas = None
        self.preview_status = tk.StringVar(self.root, value="No image loaded")
        self.preview, controls_panel = create_layout(
            self.root, self.close, self.open_image, self.save_image,
            self.select_operation, self.reset_image, self.preview_status,
        )
        self.controls = OperationControls(
            controls_panel, self.select_operation, self.apply_operation,
            self.reset_image, self.schedule_operation,
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
        self.controls.set_image_loaded(True)
        self.controls.choose("")
        self.reset_image()

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

    def require_image(self):
        if self.current_image is None:
            messagebox.showwarning(
                "No Image", "Please open an image before using this operation.",
                parent=self.root,
            )
            return False
        return True

    def cancel_processing(self):
        if self.processing_job is not None:
            self.root.after_cancel(self.processing_job)
            self.processing_job = None

    def select_operation(self, operation):
        self.cancel_processing()
        self.controls.choose(operation)
        self.apply_operation()

    def schedule_operation(self):
        if self.current_image is not None and self.processing_job is None:
            self.processing_job = self.root.after(40, self.apply_operation)

    def apply_operation(self):
        self.cancel_processing()
        if not self.require_image():
            return
        operation = self.controls.operation.get()
        try:
            parameters = self.controls.get_parameters()
        except tk.TclError:
            messagebox.showwarning("Invalid Parameter", "Use a valid slider value.", parent=self.root)
            return
        try:
            # Recompute from the original so repeated Apply/slider changes do not compound.
            if operation == "Grayscale":
                result = grayscale(self.current_image)
            elif operation == "Brightness / Contrast":
                result = brightness_contrast(self.current_image, **parameters)
            elif operation == "RGB Channels":
                result = rgb_channels(self.current_image, **parameters)
            elif operation == "Histogram Equalization":
                result = equalize_histogram(self.current_image)
            elif operation == "Median Filter":
                result = median_filter(self.current_image, **parameters)
            elif operation == "Gaussian Smoothing":
                result = gaussian_smoothing(self.current_image, **parameters)
            elif operation == "Sharpening":
                result = sharpen(self.current_image)
            elif operation == "Histogram":
                self.show_histogram()
                return
            else:
                raise ValueError("Please choose an operation.")
        except ValueError as error:
            messagebox.showwarning("Invalid Parameter", str(error), parent=self.root)
            return
        except cv2.error:
            messagebox.showerror("Processing Failed", "Could not process this image.", parent=self.root)
            return
        self.display_image = result
        status = f"Applied: {operation}"
        if parameters:
            settings = ", ".join(
                f"{name.replace('_', ' ').title()}: {float(value):g}"
                for name, value in parameters.items()
            )
            status += f"\n{settings}"
        self.preview_status.set(status)
        self.refresh_preview()
        self.update_histogram()

    def reset_image(self):
        self.cancel_processing()
        if not self.require_image():
            return
        self.controls.choose(self.controls.operation.get())
        self.display_image = self.current_image.copy()
        self.preview_status.set("Original image — no operation applied")
        self.refresh_preview()
        self.update_histogram()

    def show_histogram(self):
        if self.histogram_canvas is None or not self.histogram_canvas.winfo_exists():
            self.histogram_canvas = create_histogram_window(self.root)
        self.update_histogram()
        self.histogram_canvas.winfo_toplevel().lift()

    def update_histogram(self):
        if self.histogram_canvas is not None and self.histogram_canvas.winfo_exists():
            display_histogram(self.histogram_canvas, compute_histogram(self.display_image))

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
        self.cancel_processing()
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
            self.resize_job = None
        self.root.destroy()
