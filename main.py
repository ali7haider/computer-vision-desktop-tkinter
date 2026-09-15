"""Start the desktop computer vision application."""

import tkinter as tk

from app import ComputerVisionApp


def main():
    root = tk.Tk()
    ComputerVisionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
