# diary_module/todo_streaming.py

import pandas as pd
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import cv2

class ToDoStreaming:
    def __init__(self):
        self.setup_todo_streaming()
        self.load_todo_list()  # 클래스 초기화 시 엑셀 파일 로드

    def setup_todo_streaming(self):
        self.todo_list = None
        self.current_task_index = 0
        self.excel_file = self.get_excel_filename()
        self.show_todo_list = False
        self.blink_selected = True
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink_selected)
        self.blink_timer.start(500)

    def get_excel_filename(self):
        date_str = datetime.now().strftime("%y%m%d")
        return f'assets/todo/{date_str}.xlsx'

    def load_todo_list(self):
        try:
            self.todo_list = pd.read_excel(self.excel_file)
            self.todo_list.fillna('', inplace=True)
            self.update_todo_list()
        except FileNotFoundError:
            self.todo_list = pd.DataFrame(columns=['Task Number', 'Task Description', 'Completion Status'])
            self.update_todo_list()

    def toggle_todo_list(self, state):
        self.show_todo_list = state == Qt.Checked

    def move_up(self):
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.update_todo_list()

    def move_down(self):
        if self.current_task_index < len(self.todo_list) - 1:
            self.current_task_index += 1
            self.update_todo_list()

    def mark_done(self):
        self.todo_list.at[self.current_task_index, 'Completion Status'] = 'O'
        self.update_todo_list()
        self.save_todo_list()

    def mark_not_yet(self):
        self.todo_list.at[self.current_task_index, 'Completion Status'] = 'X'
        self.update_todo_list()
        self.save_todo_list()

    def update_todo_list(self):
        todo_text = 'To Do List:\n'
        for i, row in self.todo_list.iterrows():
            prefix = '-> ' if i == self.current_task_index else '   '
            todo_text += f"{prefix}{row['Task Number']}. {row['Task Description']} [{row['Completion Status']}]\n"
        self.todo_text = todo_text

    def save_todo_list(self):
        self.todo_list.to_excel(self.excel_file, index=False)

    def toggle_blink_selected(self):
        self.blink_selected = not self.blink_selected

    def add_todo_list(self, frame):
        overlay = frame.copy()
        alpha = 0.6
        cv2.rectangle(overlay, (0, 0), (250, 480), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        y0, dy = 30, 30
        for i, row in self.todo_list.iterrows():
            y = y0 + i * dy
            text = f"{row['Task Number']}. {row['Task Description']}"
            color = (255, 0, 0) if row['Completion Status'] != 'O' else (0, 0, 255)
            if i == self.current_task_index and self.blink_selected:
                continue
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
        return frame
