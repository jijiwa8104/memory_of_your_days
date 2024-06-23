import pandas as pd

class ToDoUpdate:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.load_tasks()
        self.current_task_index = 0  # current_task_index 속성 추가

    def load_tasks(self):
        self.todo_list = pd.read_excel(self.excel_file)
        self.todo_list.fillna('', inplace=True)

    def mark_done(self):
        self.todo_list.at[self.current_task_index, 'Completion Status'] = 'O'
        self.save_tasks()

    def mark_not_yet(self):
        self.todo_list.at[self.current_task_index, 'Completion Status'] = 'X'
        self.save_tasks()

    def save_tasks(self):
        self.todo_list.to_excel(self.excel_file, index=False)
