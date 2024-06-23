import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from todo_ui import ToDoUI
from todo_update import ToDoUpdate
from datetime import datetime
import calendar

class ToDoApp(ToDoUI):
    def __init__(self):
        super().__init__()
        today = datetime.now().strftime('%y%m%d')
        self.excel_file = f'assets/todo/{today}.xlsx'
        self.todo_update = ToDoUpdate(self.excel_file)
        self.load_tasks()

        self.add_button.clicked.connect(self.add_task)
        self.task_input.returnPressed.connect(self.add_task)  # 엔터를 누르면 add_task 호출

    def load_tasks(self):
        self.todo_update.load_tasks()
        self.update_task_list()

    def update_task_list(self):
        self.clear_layout(self.task_list_layout)
        for index, row in self.todo_update.todo_list.iterrows():
            task_text = f"{row['Task Description']}"
            self.add_task_to_layout(task_text, index, row['Completion Status'] == 'O')
        self.update_task_completion_label()

    def update_task_completion_label(self):
        total_tasks = len(self.todo_update.todo_list)
        completed_tasks = (self.todo_update.todo_list['Completion Status'] == 'O').sum()
        self.task_completion_label.setText(f'Task Completion: {completed_tasks}/{total_tasks}')

    def add_task(self):
        task_description = self.task_input.text()
        if task_description:
            self.todo_update.add_task(task_description)
            self.task_input.clear()  # 입력 필드를 비웁니다
            self.update_task_list()

    def delete_task(self, index):
        self.todo_update.delete_task(index)
        self.update_task_list()

    def move_up(self, index):
        self.todo_update.move_up(index)
        self.update_task_list()

    def move_down(self, index):
        self.todo_update.move_down(index)
        self.update_task_list()

    def update_completion_status(self, state, index):
        completion_status = 'O' if state == Qt.Checked else 'X'
        self.todo_update.update_completion_status(completion_status, index)
        self.update_task_completion_label()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToDoApp()
    ex.show()
    sys.exit(app.exec_())
