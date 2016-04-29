from ConfigParser import SafeConfigParser
import multiprocessing
from PySide.QtCore import Qt, Slot
from PySide.QtGui import QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QVBoxLayout
from server import TCP, UDP, MasterUDP

__author__ = 'LazToum'


class ServerSettings(QWidget):
    def __init__(self):
        self.pool = multiprocessing.Pool(processes=4)
        self.parser = SafeConfigParser()
        self.parser.read('settings.ini')
        self.master_port = self.parser.get('server_ports', 'master_udp')
        self.first_tcp_start = self.parser.get('server_ports', 'first_tcp_start')
        self.first_tcp_end = self.parser.get('server_ports', 'first_tcp_end')
        self.udp_start = self.parser.get('server_ports', 'udp_start')
        self.udp_end = self.parser.get('server_ports', 'udp_end')
        QWidget.__init__(self)
        self.setMinimumWidth(600)
        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        # Master UDP server settings
        self.master_port_label = QLabel("Master UDP server's Port:")
        self.grid_layout.addWidget(self.master_port_label, 1, 0)
        self.master_port_input = QLineEdit(self.master_port)
        self.master_port_input.setPlaceholderText("Default: " + self.master_port)
        self.master_port_input.displayText()
        self.grid_layout.addWidget(self.master_port_input, 1, 4)
        self.start_master_button = QPushButton('&Start Master UDP Sever')
        self.start_master_button.setStyleSheet('QPushButton {color: green;}')
        self.start_master_button.clicked.connect(self.start_master_server)
        self.grid_layout.addWidget(self.start_master_button, 1, 5)
        # First TCP server settings
        self.first_tcp_port_label = QLabel("First TCP server's Ports:")
        self.grid_layout.addWidget(self.first_tcp_port_label, 2, 0)
        self.first_tcp_port_from = QLabel("From:")
        self.grid_layout.addWidget(self.first_tcp_port_from, 2, 1)
        self.first_tcp_port_from_input = QLineEdit(self.first_tcp_start)
        self.first_tcp_port_from_input.setPlaceholderText("Default: " + self.first_tcp_start)
        self.grid_layout.addWidget(self.first_tcp_port_from_input, 2, 2)
        self.first_tcp_port_to = QLabel("To:")
        self.first_tcp_port_to.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.grid_layout.addWidget(self.first_tcp_port_to, 2, 3)
        self.first_tcp_port_to_input = QLineEdit(self.first_tcp_end)
        self.first_tcp_port_to_input.setPlaceholderText("Default: " + self.first_tcp_end)
        self.grid_layout.addWidget(self.first_tcp_port_to_input, 2, 4)
        self.start_first_tcp_button = QPushButton('&Start TCP Sever')
        # self.start_first_tcp_button.setDisabled(True)
        self.start_first_tcp_button.setStyleSheet('QPushButton {color: green;}')
        self.start_first_tcp_button.clicked.connect(self.start_first_tcp_server)
        self.grid_layout.addWidget(self.start_first_tcp_button, 2, 5)

        # Second UDP server settings
        self.udp_port_label = QLabel("UDP server's Ports:")
        self.grid_layout.addWidget(self.udp_port_label, 3, 0)
        self.udp_port_from = QLabel("From:")
        self.grid_layout.addWidget(self.udp_port_from, 3, 1)
        self.udp_port_from_input = QLineEdit(self.udp_start)
        self.udp_port_from_input.setPlaceholderText("Default: " + self.udp_start)
        self.grid_layout.addWidget(self.udp_port_from_input, 3, 2)
        self.udp_port_to = QLabel("To:")
        self.udp_port_to.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.grid_layout.addWidget(self.udp_port_to, 3, 3)
        self.udp_port_to_input = QLineEdit(self.udp_end)
        self.udp_port_to_input.setPlaceholderText("Default: " + self.udp_end)
        self.grid_layout.addWidget(self.udp_port_to_input, 3, 4)
        self.start_udp_button = QPushButton('&Start UDP Sever')
        self.start_udp_button.setStyleSheet('QPushButton {color: green;}')
        self.start_udp_button.clicked.connect(self.start_udp_server)
        self.grid_layout.addWidget(self.start_udp_button, 3, 5)

        self.layout.addLayout(self.grid_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def set_master_port(self, port):
        self.master_port = port
        self.parser.set('server_ports', 'master_udp', port)
        with open('settings.ini', 'wb') as configfile:
            self.parser.write(configfile)

    def set_first_tcp_start_port(self, port):
        self.master_port = port
        self.parser.set('server_ports', 'first_tcp_start', port)
        with open('settings.ini', 'wb') as configfile:
            self.parser.write(configfile)

    def set_first_tcp_end_port(self, port):
        self.master_port = port
        self.parser.set('server_ports', 'first_tcp_end', port)
        with open('settings.ini', 'wb') as configfile:
            self.parser.write(configfile)

    def set_udp_start_port(self, port):
        self.master_port = port
        self.parser.set('server_ports', 'udp_start', port)
        with open('settings.ini', 'wb') as configfile:
            self.parser.write(configfile)

    def set_udp_end_port(self, port):
        self.master_port = port
        self.parser.set('server_ports', 'udp_end', port)
        with open('settings.ini', 'wb') as configfile:
            self.parser.write(configfile)

    @Slot()
    def start_master_server(self):
        self.master_port_input.setDisabled(True)
        port = int(self.master_port_input.text())
        server = MasterUDP(port)
        # server = multiprocessing.Process(target=MasterUDP())
        # server.start()
        if self.start_master_button.text() == '&Start Master UDP Sever':
            self.parser.set('server_strings', 'master_status', 'on')
            with open('settings.ini', 'wb') as configfile:
                self.parser.write(configfile)
            self.start_master_button.setText('&Stop Master UDP Sever')
            self.start_master_button.setStyleSheet('QPushButton {color: red;}')
            # self.start_master_button.setDisabled(True)
            self.set_master_port(self.master_port_input.text())
            # server = MasterUDP(True)
        else:
            self.master_port_input.setDisabled(False)
            self.parser.set('server_strings', 'master_status', 'off')
            with open('settings.ini', 'wb') as configfile:
                self.parser.write(configfile)
            self.start_master_button.setText('&Start Master UDP Sever')
            self.start_master_button.setStyleSheet('QPushButton {color: green;}')
            # server = MasterUDP(False)
            server.stop()

    @Slot()
    def start_first_tcp_server(self):
        self.first_tcp_port_from_input.setDisabled(True)
        self.first_tcp_port_to_input.setDisabled(True)
        server = TCP()
        if self.start_first_tcp_button.text() == '&Start TCP Sever':
            self.start_first_tcp_button.setText('&Stop TCP Sever')
            self.start_first_tcp_button.setStyleSheet('QPushButton {color: red;}')
            # self.start_first_tcp_button.setDisabled(True)
            self.set_first_tcp_start_port(self.first_tcp_port_from_input.text())
            self.set_first_tcp_end_port(self.first_tcp_port_to_input.text())
        else:
            self.first_tcp_port_from_input.setDisabled(False)
            self.first_tcp_port_to_input.setDisabled(False)
            self.start_first_tcp_button.setText('&Start TCP Sever')
            self.start_first_tcp_button.setStyleSheet('QPushButton {color: green;}')
            server.stop()

    @Slot()
    def start_udp_server(self):
        self.udp_port_from_input.setDisabled(True)
        self.udp_port_to_input.setDisabled(True)
        # self.start_first_tcp_button.setDisabled(False)
        # self.start_first_tcp_button.setStyleSheet('QPushButton {color: green;}')
        server = UDP()
        if self.start_udp_button.text() == '&Start UDP Sever':
            self.start_udp_button.setText('&Stop UDP Sever')
            self.start_udp_button.setStyleSheet('QPushButton {color: red;}')
            # self.start_udp_button.setDisabled(True)
            self.set_udp_start_port(self.udp_port_from_input.text())
            self.set_udp_end_port(self.udp_port_to_input.text())
        else:
            self.udp_port_from_input.setDisabled(False)
            self.udp_port_to_input.setDisabled(False)
            self.start_udp_button.setText('&Start UDP Sever')
            self.start_udp_button.setStyleSheet('QPushButton {color: green;}')
            server.stop()

    def run(self):
        self.show()
