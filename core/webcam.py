"""Own the camera handle and release it on expected capture failures."""

import cv2


class Webcam:
    def __init__(self):
        self.capture = None

    def start(self):
        self.stop()
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise ValueError("Could not access the webcam. Check camera permissions and availability.")
        except (cv2.error, ValueError):
            self.stop()
            raise

    def read(self):
        if self.capture is None:
            raise ValueError("The webcam is not running.")
        try:
            success, frame = self.capture.read()
            if not success or frame is None or frame.size == 0:
                raise ValueError("Could not read a webcam frame. Check the camera and try again.")
            return frame
        except (cv2.error, ValueError):
            self.stop()
            raise

    def stop(self):
        if self.capture is not None:
            capture = self.capture
            self.capture = None
            capture.release()
