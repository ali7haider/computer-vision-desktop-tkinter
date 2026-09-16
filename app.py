"""Coordinate image state, file actions, preview, and application lifecycle."""

import tkinter as tk
from tkinter import filedialog, messagebox

import cv2

from core.file_handler import load_image, save_image
from core.webcam import Webcam
from gui.controls import OperationControls
from gui.layout import create_layout, create_histogram_window, display_histogram
from processing.color import grayscale, brightness_contrast, rgb_channels
from processing.statistics import compute_histogram, equalize_histogram
from processing.filters import median_filter, gaussian_smoothing, sharpen
from processing.edges import sobel_edges, canny_edges
from processing.segmentation import global_threshold, adaptive_threshold, detect_contours


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
        self.webcam = Webcam()
        self.webcam_running = False
        self.webcam_job = None
        self.latest_frame = None
        self.static_status = None
        self.preview_status = tk.StringVar(self.root, value="No image loaded")
        self.preview, controls_panel, self.snapshot_button, self.stop_button = create_layout(
            self.root, self.close, self.open_image, self.save_image,
            self.select_operation, self.reset_image, self.preview_status,
            self.start_webcam, self.take_snapshot, self.stop_webcam,
        )
        self.controls = OperationControls(
            controls_panel, self.select_operation, self.apply_operation,
            self.reset_image, self.schedule_operation,
            self.save_image,
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
        self.stop_webcam()
        # Preserve the loaded original separately from the result to display/save.
        self.current_image = image
        self.controls.set_image_loaded(True)
        self.controls.choose("")
        self.reset_image()

    def save_image(self):
        if self.webcam_running:
            self.warn_live_webcam()
            return
        if self.display_image is None:
            messagebox.showwarning(
                "No Image", "Please open an image before saving.", parent=self.root
            )
            return
        # Native dialogs can run pending Tk callbacks. Save the result shown now.
        image_to_save = self.display_image.copy()
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save Image As",
            defaultextension=".png",
            filetypes=IMAGE_FILE_TYPES,
        )
        if not path:
            return
        try:
            save_image(path, image_to_save)
        except (OSError, ValueError, cv2.error):
            messagebox.showerror(
                "Save Failed",
                "Could not save the image. Choose a JPG, PNG, or BMP filename "
                "in a folder where you have permission to save.",
                parent=self.root,
            )

    def require_image(self):
        if self.webcam_running:
            self.warn_live_webcam()
            return False
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
        if self.webcam_running:
            self.warn_live_webcam()
            return
        self.cancel_processing()
        self.controls.choose(operation)
        self.apply_operation()

    def schedule_operation(self):
        if not self.webcam_running and self.current_image is not None and self.processing_job is None:
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
            elif operation == "Sobel Edge Detection":
                result = sobel_edges(self.current_image, **parameters)
            elif operation == "Canny Edge Detection":
                result = canny_edges(self.current_image, **parameters)
            elif operation == "Global Thresholding":
                result = global_threshold(self.current_image, **parameters)
            elif operation == "Adaptive Thresholding":
                result = adaptive_threshold(self.current_image, **parameters)
            elif operation == "Contour Detection":
                result = detect_contours(self.current_image, **parameters)
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
            settings = []
            for name, value in parameters.items():
                try:
                    label_value = f"{float(value):g}"
                except ValueError:
                    label_value = str(value)
                settings.append(f"{name.replace('_', ' ').title()}: {label_value}")
            status += "\n" + ", ".join(settings)
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

    def warn_live_webcam(self):
        messagebox.showwarning(
            "Live Webcam", "Take a snapshot or stop the webcam before processing or saving.",
            parent=self.root,
        )

    def start_webcam(self):
        if self.webcam_running:
            return
        self.cancel_processing()
        try:
            self.webcam.start()
            frame = self.webcam.read()
        except (ValueError, cv2.error) as error:
            self.webcam.stop()
            message = str(error) if isinstance(error, ValueError) else "Could not start the webcam. Check camera permissions and availability."
            messagebox.showerror("Webcam Failed", message, parent=self.root)
            return
        self.static_status = self.preview_status.get()
        self.latest_frame = frame
        self.webcam_running = True
        self.controls.set_image_loaded(False)
        self.controls.selector.configure(state="disabled")
        self.snapshot_button.configure(state="normal")
        self.stop_button.configure(state="normal")
        self.snapshot_button.master.grid()
        # A static histogram would not describe the live preview.
        if self.histogram_canvas is not None and self.histogram_canvas.winfo_exists():
            self.histogram_canvas.winfo_toplevel().destroy()
        self.histogram_canvas = None
        self.preview_status.set("Live webcam — take a snapshot to process")
        self.refresh_preview()
        self.webcam_job = self.root.after(30, self.update_webcam)

    def update_webcam(self):
        self.webcam_job = None
        if not self.webcam_running:
            return
        try:
            self.latest_frame = self.webcam.read()
        except (ValueError, cv2.error) as error:
            self.stop_webcam()
            message = str(error) if isinstance(error, ValueError) else "Could not read a webcam frame. Check the camera and try again."
            messagebox.showerror("Webcam Failed", message, parent=self.root)
            return
        self.refresh_preview()
        self.webcam_job = self.root.after(30, self.update_webcam)

    def stop_webcam(self):
        if self.webcam_job is not None:
            self.root.after_cancel(self.webcam_job)
            self.webcam_job = None
        self.webcam.stop()
        was_running = self.webcam_running
        self.webcam_running = False
        self.latest_frame = None
        self.snapshot_button.configure(state="disabled")
        self.stop_button.configure(state="disabled")
        self.snapshot_button.master.grid_remove()
        if was_running:
            self.controls.set_image_loaded(self.current_image is not None)
            self.controls.selector.configure(state="readonly")
            self.preview_status.set(self.static_status)
            self.static_status = None
            self.refresh_preview()

    def take_snapshot(self):
        if not self.webcam_running or self.latest_frame is None:
            messagebox.showwarning("No Webcam Frame", "Start the webcam before taking a snapshot.", parent=self.root)
            return
        image = self.latest_frame.copy()
        self.stop_webcam()
        self.current_image = image
        self.controls.set_image_loaded(True)
        self.controls.choose("")
        self.reset_image()

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
        image = self.latest_frame if self.webcam_running else self.display_image
        if image is None:
            self.preview.create_text(
                width / 2, height / 2, text="Open an image or access the webcam to begin.",
                fill="#64748B", width=width,
            )
            return

        image_height, image_width = image.shape[:2]
        scale = min(width / image_width, height / image_height, 1.0)
        size = (max(1, int(image_width * scale)), max(1, int(image_height * scale)))
        preview_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        color_code = cv2.COLOR_GRAY2RGB if preview_image.ndim == 2 else cv2.COLOR_BGR2RGB
        rgb_image = cv2.cvtColor(preview_image, color_code)
        # Tkinter reads PPM directly; no extra image-display dependency is needed.
        ppm = f"P6\n{size[0]} {size[1]}\n255\n".encode("ascii") + rgb_image.tobytes()
        self.preview_photo = tk.PhotoImage(master=self.root, data=ppm, format="PPM")
        self.preview.create_image(width / 2, height / 2, image=self.preview_photo)

    def close(self):
        self.cancel_processing()
        self.stop_webcam()
        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)
            self.resize_job = None
        self.root.destroy()
