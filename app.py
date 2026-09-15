"""Coordinate the application window and its lifecycle."""

from gui.layout import create_layout


class ComputerVisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Computer Vision Tool")
        self.root.geometry("1000x650")
        self.root.minsize(700, 450)
        create_layout(self.root, self.close)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        self.root.destroy()
