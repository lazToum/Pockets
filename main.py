#!/usr/bin/python2
import multiprocessing
import os
import sys
from ConfigParser import SafeConfigParser
from PySide import QtGui

import modules.class_tab as class_tab
import modules.client_tab as client_tab
import modules.logs_tab as logs_tab
import modules.report_tab as report_tab
import modules.settings_window as settings_window
from PySide.QtCore import QFileSystemWatcher, Slot
from PySide.QtGui import QTabWidget, QMenuBar, QMainWindow
from modules.logs import Log

from modules import server_settings_tab

__author__ = 'lazToum'


class Pockets(QMainWindow):
    def __init__(self):
        self.pool = multiprocessing.Pool(processes=6)
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.class_day = parser.get('class_settings', 'ClassDay')
        self.class_hours = parser.get('class_settings', 'ClassHours')
        self.exam_part = parser.get('class_settings', 'ExamPart')
        QMainWindow.__init__(self)
        self.tab5 = client_tab.ClientSettings()
        self.tab4 = report_tab.Reports()
        self.tab3 = logs_tab.ServerLogs()
        self.tab2 = server_settings_tab.ServerSettings()
        self.tab1 = class_tab.SelectClass()
        self.logs = Log()
        self.settings = settings_window.Settings()
        self.content_widget = QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout()
        self.menu_bar = QMenuBar(self)
        self.tabs = QTabWidget(self)
        self.setWindowTitle('PySockets')
        desktop = QtGui.QApplication.desktop()
        self.setMaximumWidth(desktop.width())
        self.setMinimumWidth(desktop.width() - desktop.width() / 4)
        watch_paths = [os.getcwd() + '/logs', os.getcwd() + '/logs/' + self.class_day + '/' + self.class_hours +
                       '/' + self.exam_part + 'MasterUDPLog.txt', os.getcwd() + '/logs/' + self.class_day + '/' +
                       self.class_hours + '/' + self.exam_part + 'TCPLog.txt', os.getcwd() + '/logs/' +
                       self.class_day + '/' + self.class_hours + '/' + self.exam_part + 'UDPLog.txt']
        self.fs_watcher = QFileSystemWatcher(watch_paths)
        self.fs_watcher.directoryChanged.connect(self.add_file)
        self.fs_watcher.fileChanged.connect(self.tab3.update)
        # fs_watcher.connect(fs_watcher, SIGNAL('fileChanged(QString)'), self.logs.update)
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.tabs.addTab(self.tab1, "Class Initialization")
        self.tabs.addTab(self.tab2, "Servers' Settings")
        self.tabs.addTab(self.tab5, "Clients' Settings")
        self.tabs.addTab(self.tab3, "Servers' Logs")
        # self.tabs.addTab(self.tab4, "Exam Report")
        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.tabs)
        self.content_widget.setLayout(self.layout)
        self.setCentralWidget(self.content_widget)

    def create_menu(self):
        # settings action menu item
        settings_action = QtGui.QAction('&Settings', self)
        settings_action.setShortcut('Ctrl+S')
        settings_action.setStatusTip('Settings')
        settings_action.triggered.connect(self.settings_open)

        # exit action menu item
        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        # about action menu item
        about_action = QtGui.QAction('About', self)
        about_action.setShortcut('Ctrl+A')
        about_action.setStatusTip('About')
        about_action.triggered.connect(self.about)

        file_menu = self.menu_bar.addMenu('&File')
        file_menu.addAction(settings_action)
        file_menu.addAction(exit_action)
        file_menu.addAction(about_action)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'Exit',
                                           "Are you sure you want to exit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @staticmethod
    def about():
        QtGui.QMessageBox.information(QtGui.QMessageBox(), 'About Sockets',
                                      "Version 1.1" + '\n' + "Created by Lazaros Toumanidis" + '\n')

    def settings_open(self):
        self.settings.show()

    @Slot()
    def add_file(self):
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.class_day = parser.get('class_settings', 'ClassDay')
        self.class_hours = parser.get('class_settings', 'ClassHours')
        self.exam_part = parser.get('class_settings', 'ExamPart')
        self.fs_watcher.addPath(os.getcwd() + '/logs/' + self.class_day)
        self.fs_watcher.addPath(os.getcwd() + '/logs/' + self.class_day + '/' + self.class_hours)
        self.fs_watcher.addPath(
                os.getcwd() + '/logs/' + self.class_day + '/' + self.class_hours + '/' + self.exam_part +
                'MasterUDPLog.txt')
        self.fs_watcher.addPath(
                os.getcwd() + '/logs/' + self.class_day + '/' + self.class_hours + '/' + self.exam_part + 'TCPLog.txt')
        self.fs_watcher.addPath(
                os.getcwd() + '/logs/' + self.class_day + '/' + self.class_hours + '/' + self.exam_part + 'UDPLog.txt')

    def run(self):
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    app.processEvents()
    ex = Pockets()
    ex.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
