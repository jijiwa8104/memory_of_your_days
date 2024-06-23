# diary_module/diary_ui.py

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import threading
import os
from datetime import datetime
import pandas as pd
from video_recording import VideoRecording
from blinking_indicator import BlinkingIndicator
from todo_streaming import ToDoStreaming

class VideoRecorder(QWidget, VideoRecording, BlinkingIndicator, ToDoStreaming):
    def __init__(self):
        super().__init__()
        VideoRecording.__init__(self)
        BlinkingIndicator.__init__(self)
        ToDoStreaming.__init__(self)
        self.initUI()
        self.load_todo_list()  # 프로그램 실행 시 오늘 날짜의 엑셀 파일 불러오기

    def initUI(self):
        self.setWindowTitle('Video Recorder')
        self.setGeometry(100, 100, 800, 600)

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton('Stop Recording', self)
        self.stop_button.clicked.connect(self.stop_recording)

        self.label = QLabel(self)
        self.label.resize(640, 480)

        self.todo_checkbox = QCheckBox('Show To Do List', self)
        self.todo_checkbox.stateChanged.connect(self.toggle_todo_list)

        self.update_button = QPushButton('Update List', self)
        self.update_button.clicked.connect(self.load_todo_list)

        self.up_button = QPushButton('Up', self)
        self.up_button.clicked.connect(self.move_up)

        self.down_button = QPushButton('Down', self)
        self.down_button.clicked.connect(self.move_down)

        self.done_button = QPushButton('Done', self)
        self.done_button.clicked.connect(self.mark_done)

        self.notyet_button = QPushButton('Not Yet', self)
        self.notyet_button.clicked.connect(self.mark_not_yet)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.todo_checkbox)
        control_layout.addWidget(self.update_button)

        todo_layout = QVBoxLayout()
        todo_layout.addWidget(self.up_button)
        todo_layout.addWidget(self.down_button)
        todo_layout.addWidget(self.done_button)
        todo_layout.addWidget(self.notyet_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(control_layout)
        layout.addLayout(todo_layout)

        self.setLayout(layout)

    def closeEvent(self, event):
        self.streaming = False
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()
