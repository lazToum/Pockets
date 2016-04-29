from ConfigParser import SafeConfigParser
import os
import errno

__author__ = 'lary'


class Exam:
    def __init__(self):
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.class_day = parser.get('class_settings', 'ClassDay')
        self.class_hours = parser.get('class_settings', 'ClassHours')
        self.exam_part = parser.get('class_settings', 'ExamPart')
        if parser.get('class_settings', 'AssociationsFile') == 'SocketsApp/associations.csv':
            self.associations_file = os.getcwd()+'/' + parser.get('class_settings', 'AssociationsFile')
        else:
            self.associations_file = parser.get('class_settings', 'AssociationsFile')
        self.init_reports()

    def get_class_day(self):
        return self.class_day

    def get_class_hours(self):
        return self.class_hours

    def get_exam_part(self):
        return self.exam_part

    def get_associations_file(self):
        return self.associations_file

    def set_class_day(self, day):
        self.class_day = day

    def set_class_hours(self, hours):
        self.class_hours = hours

    def set_exam_part(self, part):
        self.exam_part = part

    def set_associations_file(self, associations_file):
        self.associations_file = associations_file

    def init_reports(self):
        class_day = self.class_day
        class_hours = self.class_hours
        exam_part = self.exam_part
        directory_to_make = './logs/' + class_day + '/' + class_hours
        if not os.path.isdir(directory_to_make):
            try:
                os.makedirs(directory_to_make)
            except os.error, e:
                if e.errno != errno.EEXIST:
                    pass
        master_log = directory_to_make + '/' + exam_part + 'MasterUDPLog.txt'
        first_tcp_log = directory_to_make + '/' + exam_part + 'TCPLog.txt'
        udp_log = directory_to_make + '/' + exam_part + 'UDPLog.txt'
        with open(master_log, 'ab') as logfile:
            logfile.write('')
            logfile.close()
        with open(first_tcp_log, 'ab') as logfile:
            logfile.write('')
            logfile.close()
        with open(udp_log, 'ab') as logfile:
            logfile.write('')
            logfile.close()

    def __str__(self):
        return "Class day: : %s, Class hours: %s,  Exam Part: %s, Associations File: %s" % (
            self.class_day, self.class_hours, self.exam_part, self.associations_file)
