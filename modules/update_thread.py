from PySide.QtCore import QThread, Signal
import time
from PySide.QtGui import QVBoxLayout, QProgressBar, QLabel, QDialog

__author__ = 'lazToum'


class TestDialog(QDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)

        self.statusText = QLabel()
        self.progressBar = QProgressBar()

        layout = QVBoxLayout()
        layout.addWidget(self.statusText)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

        self.thread = TestThread()
        self.thread.indexFinished.connect(self.update_progress)
        self.thread.finished.connect(self.close)
        self.thread.start()

    def update_progress(self, value, total):
        self.statusText.setText('{} of {} completed'.format(value, total))
        self.progressBar.setValue(value)


class TestThread(QThread):
    indexFinished = Signal(int, int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self.test_list = range(1, 101)

    def run(self):
        for i in self.test_list:
            self.indexFinished.emit(i, len(self.test_list))
            time.sleep(.1)
