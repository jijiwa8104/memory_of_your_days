# diary_module/diary_app.py

import sys
from PyQt5.QtWidgets import QApplication
from diary_ui import VideoRecorder

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoRecorder()
    ex.show()
    sys.exit(app.exec_())
