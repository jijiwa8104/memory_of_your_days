import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from subprocess import Popen

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SMILE_MENU')
        self.setGeometry(100, 100, 400, 400)
        
        button_size = 200
        
        self.todo_button = QPushButton('To Do', self)
        self.todo_button.setFixedSize(button_size, button_size)
        self.todo_button.clicked.connect(self.start_todo_program)
        
        self.diary_button = QPushButton('Diary', self)
        self.diary_button.setFixedSize(button_size, button_size)
        self.diary_button.clicked.connect(self.start_diary_program)

        layout = QHBoxLayout()
        layout.addWidget(self.todo_button)
        layout.addWidget(self.diary_button)
        
        self.setLayout(layout)

    def start_todo_program(self):
        Popen([sys.executable, 'todo_module/todo_app.py'])

    def start_diary_program(self):
        Popen([sys.executable, 'diary_module/diary_app.py'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
