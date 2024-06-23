# diary_module/blinking_indicator.py

import cv2
from PyQt5.QtCore import QTimer

class BlinkingIndicator:
    def __init__(self):
        self.setup_blinking_indicator()

    def setup_blinking_indicator(self):
        self.red_dot_timer = QTimer(self)
        self.red_dot_timer.timeout.connect(self.blink_red_dot)
        self.red_dot_visible = False

    def blink_red_dot(self):
        self.red_dot_visible = not self.red_dot_visible

    def add_red_dot(self, frame):
        if self.red_dot_visible:
            height, width, _ = frame.shape
            cv2.circle(frame, (width - 20, 20), 10, (0, 0, 255), -1)
        return frame
