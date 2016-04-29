from ConfigParser import SafeConfigParser
import os
from PySide import QtGui, QtCore
from PySide.QtCore import Slot
from PySide.QtGui import QWidget, QVBoxLayout, QComboBox, QGridLayout, QLabel, QLineEdit, QPushButton

__author__ = 'lazToum'


class Settings(QWidget):
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read('settings.ini')
        self.class_day = self.parser.get('class_settings', 'ClassDay')
        self.class_hour = self.parser.get('class_settings', 'ClassHours')
        self.exam_part = self.parser.get('class_settings', 'ExamPart')
        self.current = self.parser.items('Client_Effects')
        QWidget.__init__(self)
        self.effects = [self.parser.get('Message_Effects', '0'), self.parser.get('Message_Effects', '1'),
                        self.parser.get('Message_Effects', '2'), self.parser.get('Message_Effects', '3'),
                        self.parser.get('Message_Effects', '4')]
        self.setWindowTitle('Settings')
        self.setMinimumWidth(600)
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.selected_client = QComboBox(self)
        self.selected_client.addItem('Select Client')
        for i in range(0, len(self.current)):
            self.selected_client.addItem(self.current[i][0])
        grid_layout.addWidget(self.selected_client, 0, 0)
        self.connect(self.selected_client, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.show_selection)
        tcp_message_label = QLabel('TCP Message to send:')
        grid_layout.addWidget(tcp_message_label, 0, 1)
        self.tcp_input = QLineEdit('')
        self.tcp_input.setDisabled(True)
        self.tcp_input.setPlaceholderText('TCP message')
        grid_layout.addWidget(self.tcp_input, 0, 2)
        udp_message_label = QLabel('UDP Message to send:')
        grid_layout.addWidget(udp_message_label, 0, 3)
        self.udp_input = QLineEdit('')
        self.udp_input.setDisabled(True)
        self.udp_input.setPlaceholderText('UDP message')
        grid_layout.addWidget(self.udp_input, 0, 4)
        effect_label = QLabel('Effect:')
        grid_layout.addWidget(effect_label, 0, 5)
        self.effects_list = QComboBox(self)
        self.effects_list.addItems(self.effects)
        self.effects_list.setCurrentIndex(1)
        self.effects_list.setDisabled(True)
        grid_layout.addWidget(self.effects_list, 0, 6)
        save_button = QPushButton('&Save')
        save_button.clicked.connect(self.save)
        grid_layout.addWidget(save_button, 0, 7)
        layout.addLayout(grid_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    @Slot()
    def show_selection(self):
        if self.selected_client.currentIndex() != 0:
            if self.parser.has_option('Client_TCP_Settings', self.current[self.selected_client.currentIndex() - 1][0]):
                self.tcp_input.setText(
                    self.parser.get('Client_TCP_Settings', self.current[self.selected_client.currentIndex() - 1][0]))
                self.tcp_input.setDisabled(False)
                self.udp_input.setText(
                    self.parser.get('Client_UDP_Settings', self.current[self.selected_client.currentIndex() - 1][0]))
                self.udp_input.setDisabled(False)
                self.effects_list.setCurrentIndex(self.effects.index(self.parser.get(
                        'Message_Effects',
                        self.parser.get('Client_Effects', self.current[self.selected_client.currentIndex() - 1][0]))))
                self.effects_list.setDisabled(False)
        else:
            self.tcp_input.setText('TCP message')
            self.tcp_input.setDisabled(True)
            self.udp_input.setText('UDP message')
            self.udp_input.setDisabled(True)
            self.effects_list.setCurrentIndex(1)
            self.effects_list.setDisabled(True)
            self.special_checkbox.setChecked(False)
            self.special_checkbox.setDisabled(True)

    @Slot()
    def save(self):
        if self.parser.has_option('Client_TCP_Settings', self.current[self.selected_client.currentIndex() - 1][0]):
            self.parser.set('Client_TCP_Settings', self.current[self.selected_client.currentIndex() - 1][0],
                            self.tcp_input.text())
            self.parser.set('Client_UDP_Settings', self.current[self.selected_client.currentIndex() - 1][0],
                            self.udp_input.text())
            self.parser.set('Client_Effects', self.current[self.selected_client.currentIndex() - 1][0],
                            str(self.effects_list.currentIndex()))
            with open('settings.ini', 'wb') as configfile:
                self.parser.write(configfile)
        else:
            pass

    def run(self):
        # Show the form
        self.show()
