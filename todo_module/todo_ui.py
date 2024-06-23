from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from datetime import datetime
import calendar
from todo_update import ToDoUpdate  # ToDoUpdate 클래스 import

class ToDoUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.checkboxes = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To Do List')
        self.setGeometry(60, 80, 800, 850)  # 창 크기를 800x850로 설정

        self.title = QLabel('To Do List', self)
        self.title.setAlignment(Qt.AlignCenter)  # 가운데 정렬
        self.title.setStyleSheet("font-size: 48px;")  # 글자 크기 3배 (48px)

        today = datetime.now()
        date_str = today.strftime('%y%m%d')
        day_name = calendar.day_name[today.weekday()]
        date_display = today.strftime(f'%y.%m.%d ({day_name[:3]})')

        self.date_label = QLabel(f'Date: {date_display}', self)
        self.date_label.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.date_label.setStyleSheet("font-size: 32px;")  # 글자 크기 2배 (32px)

        self.task_list_layout = QVBoxLayout()

        self.task_input = QLineEdit(self)
        self.add_button = QPushButton('ADD', self)
        self.task_completion_label = QLabel('Task Completion: 0/0', self)

        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel('To Do:'))
        control_layout.addWidget(self.task_input)
        control_layout.addWidget(self.add_button)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.date_label)
        layout.addLayout(self.task_list_layout)
        layout.addWidget(self.task_completion_label)
        layout.addLayout(control_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_task_to_layout(self, task_text, index, checked):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_widget.setStyleSheet("background-color: lightgray;")

        delete_button = QPushButton('X', self)
        delete_button.setFixedSize(30, 60)  # 세로로 길쭉한 직사각형 모양
        delete_button.clicked.connect(lambda _, idx=index: self.delete_task(idx))

        move_buttons_widget = QWidget()
        move_buttons_layout = QVBoxLayout(move_buttons_widget)
        move_buttons_layout.setContentsMargins(0, 0, 0, 0)

        move_up_button = QPushButton('↑', self)
        move_up_button.setFixedSize(60, 30)  # 가로로 길쭉한 모양
        move_up_button.clicked.connect(lambda _, idx=index: self.move_up(idx))

        move_down_button = QPushButton('↓', self)
        move_down_button.setFixedSize(60, 30)  # 가로로 길쭉한 모양
        move_down_button.clicked.connect(lambda _, idx=index: self.move_down(idx))

        move_buttons_layout.addWidget(move_up_button)
        move_buttons_layout.addWidget(move_down_button)

        task_label = QLabel(task_text, self)
        task_label.setStyleSheet("font-size: 24px;")  # 글자 크기 설정

        # 스페이스바 3개 정도의 간격을 추가합니다.
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        checkbox = QCheckBox(self)
        checkbox.setStyleSheet(
            "QCheckBox::indicator {"
            "width: 80px;"
            "height: 80px;"
            "}"
        )  # 체크박스 크기를 두 배로 조절
        checkbox.setChecked(checked)
        checkbox.stateChanged.connect(lambda state, idx=index: self.update_completion_status(state, idx))

        row_layout.addWidget(delete_button)
        row_layout.addWidget(move_buttons_widget)
        row_layout.addItem(spacer)
        row_layout.addWidget(task_label)
        row_layout.addStretch(1)
        row_layout.addWidget(checkbox, alignment=Qt.AlignRight)  # 체크박스를 오른쪽 끝으로 고정

        self.task_list_layout.addWidget(row_widget)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
