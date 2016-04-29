from PySide.QtCore import Qt, Slot
from PySide.QtGui import QWidget, QVBoxLayout, QPlainTextEdit
from exam import Exam

__author__ = 'lazToum'


class Log(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        exam = Exam()
        exam.init_reports()
        self.layout = QVBoxLayout()
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.console)
        self.setLayout(self.layout)

    @Slot()
    def update(self, path):
        print path
        with open(path) as fopen:
            data = fopen.read()
        self.console.setPlainText(data)
