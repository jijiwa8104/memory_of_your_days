import pandas as pd
import os

class ToDoUpdate:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.load_tasks()
        self.current_task_index = 0  # current_task_index 속성 추가

    def load_tasks(self):
        if not os.path.exists(self.excel_file):
            # 파일이 없으면 새로운 파일을 생성하고 열 제목을 추가합니다.
            self.todo_list = pd.DataFrame(columns=['Task Number', 'Task Description', 'Completion Status'])
            self.save_tasks()
        else:
            self.todo_list = pd.read_excel(self.excel_file)
        self.todo_list.fillna('', inplace=True)

    def add_task(self, description):
        new_task = {'Task Number': len(self.todo_list) + 1, 'Task Description': description, 'Completion Status': 'X'}
        new_task_df = pd.DataFrame([new_task])
        self.todo_list = pd.concat([self.todo_list, new_task_df], ignore_index=True)
        self.reindex_task_numbers()
        self.save_tasks()

    def delete_task(self, index):
        self.todo_list = self.todo_list.drop(index)
        self.todo_list.reset_index(drop=True, inplace=True)
        self.reindex_task_numbers()
        self.save_tasks()

    def move_up(self, index):
        if index > 0:
            self.todo_list.iloc[index - 1], self.todo_list.iloc[index] = self.todo_list.iloc[index], self.todo_list.iloc[index - 1]
            self.reindex_task_numbers()
            self.save_tasks()

    def move_down(self, index):
        if index < len(self.todo_list) - 1:
            self.todo_list.iloc[index + 1], self.todo_list.iloc[index] = self.todo_list.iloc[index], self.todo_list.iloc[index + 1]
            self.reindex_task_numbers()
            self.save_tasks()

    def update_completion_status(self, status, index):
        self.todo_list.at[index, 'Completion Status'] = status
        self.save_tasks()

    def save_tasks(self):
        self.todo_list.to_excel(self.excel_file, index=False)

    def reindex_task_numbers(self):
        self.todo_list['Task Number'] = range(1, len(self.todo_list) + 1)
