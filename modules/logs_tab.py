from ConfigParser import SafeConfigParser
from PySide.QtCore import Qt
from PySide.QtGui import QTabWidget, QPlainTextEdit, QVBoxLayout, QWidget

__author__ = 'lazToum'


class ServerLogs(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.class_day = parser.get('class_settings', 'ClassDay')
        self.class_hours = parser.get('class_settings', 'ClassHours')
        self.exam_part = parser.get('class_settings', 'ExamPart')
        master_console_widget = QWidget()
        self.master_console = QPlainTextEdit()
        self.master_console.setReadOnly(True)
        self.master_console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        master_tab_layout = QVBoxLayout()
        master_tab_layout.addWidget(self.master_console)
        master_console_widget.setLayout(master_tab_layout)
        self.tab1 = master_console_widget
        tcp_console_widget = QWidget()
        self.tcp_console = QPlainTextEdit()
        self.tcp_console.setReadOnly(True)
        self.tcp_console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tcp_tab_layout = QVBoxLayout()
        tcp_tab_layout.addWidget(self.tcp_console)
        tcp_console_widget.setLayout(tcp_tab_layout)
        self.tab2 = tcp_console_widget
        udp_console_widget = QWidget()
        self.udp_console = QPlainTextEdit()
        self.udp_console.setReadOnly(True)
        self.udp_console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        udp_tab_layout = QVBoxLayout()
        udp_tab_layout.addWidget(self.udp_console)
        udp_console_widget.setLayout(udp_tab_layout)
        self.tab3 = udp_console_widget
        self.addTab(self.tab1, 'Master UDP')
        self.addTab(self.tab2, 'TCP')
        self.addTab(self.tab3, 'UDP')
        self.setMinimumWidth(800)

    def run(self):
        self.show()

    def update(self, path):
        with open(path) as fopen:
                data = fopen.read()
        server_test = path[-16:]
        if server_test == 'MasterUDPLog.txt':
            self.master_console.setPlainText(data)
        elif path[-10:] == 'UDPLog.txt':
            self.udp_console.setPlainText(data)
        elif path[-10:] == 'TCPLog.txt':
            self.tcp_console.setPlainText(data)
        else:
            pass