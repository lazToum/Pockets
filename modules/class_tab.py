import exam
import os
import sys
from ConfigParser import SafeConfigParser
from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *
__author__ = 'lazToum'


class SelectClass(QWidget):
    def __init__(self):
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.class_day = parser.get('class_settings', 'ClassDay')
        self.class_hour = parser.get('class_settings', 'ClassHours')
        self.exam_part = parser.get('class_settings', 'ExamPart')
        # if parser.get('class_settings', 'AssociationsFile') == 'SocketsApp/associations.xlsx':
        #     self.associations_file = os.getcwd()+'/' + parser.get('class_settings', 'AssociationsFile')
        # else:
        #     self.associations_file = parser.get('class_settings', 'AssociationsFile')
        self.exam_window = QtGui.QWidget()
        QWidget.__init__(self)
        self.setMinimumWidth(400)
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.days_of_week = ['Monday',
                             'Tuesday',
                             'Wednesday',
                             'Thursday',
                             'Friday',
                             'Saturday',
                             'Sunday']
        self.day = QComboBox(self)
        self.day.addItems(self.days_of_week)
        self.day.setCurrentIndex(self.days_of_week.index(self.class_day))
        self.form_layout.addRow('Select Day:', self.day)
        self.class_hours = ['09-11',
                            '11-13',
                            '13-15',
                            '15-17',
                            '17-19',
                            '19-21']

        self.hour = QComboBox(self)
        self.hour.addItems(self.class_hours)
        self.hour.setCurrentIndex(self.class_hours.index(self.class_hour))
        self.form_layout.addRow('Class TIme:', self.hour)

        self.class_parts = ['A',
                            'B',
                            'C',
                            'D']

        self.class_part = QComboBox(self)
        self.class_part.addItems(self.class_parts)
        self.form_layout.addRow('Exam Part:', self.class_part)
        self.class_part.setCurrentIndex(self.class_parts.index(self.exam_part))
        self.connect(self.day, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.show_selection)
        self.connect(self.hour, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.show_selection)
        self.connect(self.class_part, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.show_selection)

        self.exam = QLabel('%s, %s, Part %s' %
                           (self.days_of_week[self.day.currentIndex()],
                            self.class_hours[self.hour.currentIndex()],
                            self.class_parts[self.class_part.currentIndex()]), self)
        self.form_layout.addRow('Exam Selected:', self.exam)
        self.layout.addLayout(self.form_layout)

        # self.file_button_box = QGridLayout()
        # self.empty_label = QLabel("")
        # self.file_button = QPushButton('&Select xls(x) file to use', self)
        # self.file_button.clicked.connect(self.select_file)
        # self.file_button_box.addWidget(self.empty_label, 0, 0)
        # self.file_button_box.addWidget(self.file_button, 0, 1)
        # self.file_button_box.addWidget(self.empty_label, 0, 2)
        # self.layout.addLayout(self.file_button_box)
        #
        # self.make_button_box = QGridLayout()
        # self.empty_label = QLabel("")
        # self.exam_button = QPushButton('&Make Exam Folders and Files', self)
        # self.exam_button.clicked.connect(self.start_exam)
        # self.make_button_box.addWidget(self.empty_label, 0, 0)
        # self.make_button_box.addWidget(self.exam_button, 0, 1)
        # self.make_button_box.addWidget(self.empty_label, 0, 2)
        # self.layout.addLayout(self.make_button_box)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def set_class_day(self, day):
        self.class_day = day
        parser = SafeConfigParser()
        parser.read('settings.ini')
        parser.set('class_settings', 'ClassDay', day)
        with open('settings.ini', 'wb') as configfile:
            parser.write(configfile)

    def set_class_hours(self, hour):
        self.class_hour = hour
        parser = SafeConfigParser()
        parser.read('settings.ini')
        parser.set('class_settings', 'ClassHours', hour)
        with open('settings.ini', 'wb') as configfile:
            parser.write(configfile)

    def set_exam_part(self, part):
        self.exam_part = part
        parser = SafeConfigParser()
        parser.read('settings.ini')
        parser.set('class_settings', 'ExamPart', part)
        with open('settings.ini', 'wb') as configfile:
            parser.write(configfile)

    def get_class_day(self):
        return self.class_day

    def get_class_hours(self):
        return self.class_hour

    def get_exam_part(self):
        return self.exam_part

    # def get_associations_file(self):
    #     return self.associations_file

    @Slot()
    def show_selection(self):
        class_day = self.days_of_week[self.day.currentIndex()]
        class_hours = self.class_hours[self.hour.currentIndex()]
        exam_part = self.class_parts[self.class_part.currentIndex()]
        self.exam.setText('%s, %s, Part %s' % (class_day, class_hours, exam_part))
        self.set_class_day(class_day)
        self.set_class_hours(class_hours)
        self.set_exam_part(exam_part)

    # @Slot()
    # def select_file(self):
    #     path, _ = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
    #     if path == '':
    #         path = 'SocketsApp/associations.xlsx'
    #     self.set_associations_file(path)

    # @Slot()
    # def start_exam(self):
    #     exam.Exam()

    def run(self):
        # Show the form
        self.show()
