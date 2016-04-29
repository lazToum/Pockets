# coding=utf-8
from ConfigParser import SafeConfigParser
from random import randint
from PySide import QtCore
from PyQt4.QtCore import QObject, QThread
import socket
import sys
import select
import time
import math
from exam import Exam


def get_exam(server_type):
    parser = SafeConfigParser()
    parser.read('settings.ini')
    class_day = parser.get('class_settings', 'ClassDay')
    class_hours = parser.get('class_settings', 'ClassHours')
    exam_part = parser.get('class_settings', 'ExamPart')

    return {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part, 'server_type': server_type}


def clear_log(exam_settings):
    with open('logs/' + exam_settings['class_day'] + '/' + exam_settings['class_hours'] + '/' +
              exam_settings['exam_part'] + exam_settings['server_type'] + 'Log.txt', 'wb') as log_file:
        log_file.write('')


def write_log(exam_settings, text):
    with open('logs/' + exam_settings['class_day'] + '/' + exam_settings['class_hours'] + '/' +
              exam_settings['exam_part'] + exam_settings['server_type'] + 'Log.txt', 'ab') as log_file:
        log_file.write(text)


def servers_standard_format(server_type, servers_data=None):
    if not servers_data:
        servers_data = []
    if len(servers_data) == 0:
        servers_format = '{:22s} '.format(server_type + ' server started') + ' \n \n '
        servers_format += '{:_^7} | {:_^8} | {:_^30} | {:_^30} | {:_^31} | {:_^16} | {:_^24} | {:_^25}'.format(
            '#', 'Reg Id', 'Client\'s IP:PORT', 'Server\'s IP:PORT', 'TimeStamp', 'Hostname', 'Message Received',
            'Message Sent')
        servers_format += '\n'
    elif len(servers_data) == 1:
        servers_format = ' ' * 87 + ' | ' + '(' + time.ctime() + ') ' + servers_data[0]
    else:
        servers_format = '{:_^7} | {:_^8} | {:_^29} | {:_^29} | {:_^34} | {:_^15} | {:_^25} | {:_^24}'.format(
            servers_data[0], servers_data[1], servers_data[2] + ':' + servers_data[3], servers_data[4] + ':' + servers_data[5],
            time.ctime(), servers_data[6], servers_data[7], servers_data[8])
    return servers_format + '\n'


def expected_client(client_ip, server_port, server_type):
    parser = SafeConfigParser()
    parser.read('settings.ini')
    if parser.has_option('Server_Client_' + server_type + '_Ports', client_ip):
        return parser.get('Server_Client_' + server_type + '_Ports', client_ip) == server_port
    else:
        return False


def server_effect_and_message(client_ip, server_type, message_received):
    effected_message = message_received
    client_ip = str(client_ip)
    parser = SafeConfigParser()
    parser.read('settings.ini')
    if parser.has_option('Client_' + server_type + '_Settings', client_ip):
        message_to_send = parser.get('Client_' + server_type + '_Settings', client_ip)
    else:
        message_to_send = ' '
    if parser.has_option('Client_CTRL_Chars', client_ip):
        ctrl_required = parser.get('Client_CTRL_Chars', client_ip) == '1'
        if ctrl_required:
            message_to_send += parser.get('CTRL_Chars', str(randint(1, 25)))

    if parser.has_option('Client_Effects', client_ip):
        effect_number = parser.get('Client_Effects', client_ip)
        if effect_number == '0':
            effect = str(randint(1, 5))
            if effect == '1':
                effected_message = message_received
            elif effect == '2':
                effected_message = message_received.upper()
            elif effect == '3':
                effected_message = message_received.lower()
            elif effect == '4':
                effected_message = str(len(message_received))
            else:
                effected_message = message_received[1:-1]
    else:
        effected_message = message_received.upper()
    return {'to_send': message_to_send, 'effected': effected_message}


class MasterUDP(QObject):
    def __init__(self, port):
        QObject.__init__(self)
        self.updateThread = MasterThread(port)
        self.setup_update_thread()

    def setup_update_thread(self):
        if not self.updateThread.isRunning():
            self.updateThread.start()

    def stop(self):
        self.updateThread.exiting = True
        self.updateThread.terminate()


class MasterThread(QThread):
    progress = QtCore.Signal(str)

    def __init__(self, port, parent=None):
        self.running = True
        exam = Exam()
        exam.init_reports()
        self.parser = SafeConfigParser()
        self.parser.read('settings.ini')
        class_day = self.parser.get('class_settings', 'ClassDay')
        class_hours = self.parser.get('class_settings', 'ClassHours')
        exam_part = self.parser.get('class_settings', 'ExamPart')
        self.exam = {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part,
                     'server_type': 'MasterUDP'}
        clear_log(self.exam)
        write_log(self.exam, servers_standard_format('MasterUDP'))
        self.port = port
        self.connections_counter = 1
        super(MasterThread, self).__init__(parent)

    def run(self):
        connections_counter = self.connections_counter
        server_port = self.port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, socket.SO_REUSEPORT)
            server_socket.bind(('', server_port))
            while self.running:
                what_to_print, client_address = server_socket.recvfrom(1024)
                log = '{:_^7}'.format(connections_counter) + ' ' + what_to_print
                write_log(self.exam, log)
                connections_counter += 1
        except socket.error:
            server_socket.close()
            self.exit()

    def stop(self):
        self.running = False
        self.socket.shutdown()


class TCP(QObject):
    def __init__(self):
        QObject.__init__(self)
        parser = SafeConfigParser()
        parser.read('settings.ini')
        class_day = parser.get('class_settings', 'ClassDay')
        class_hours = parser.get('class_settings', 'ClassHours')
        exam_part = parser.get('class_settings', 'ExamPart')
        exam = {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part,
                'server_type': 'TCP'}
        clear_log(exam)
        write_log(exam, servers_standard_format('TCP'))
        start_port = int(parser.get('server_ports', 'first_tcp_start'))
        end_port = int(parser.get('server_ports', 'first_tcp_end'))
        server_ports = []
        if end_port < start_port:
            swap = end_port
            end_port = start_port
            start_port = swap
        for i in range(end_port - start_port + 1):
            server_ports.append(start_port + i)
        self.updateThread = TCPThread(server_ports)
        self.setup_update_thread()

    def setup_update_thread(self):
        if not self.updateThread.isRunning():
            self.updateThread.start()

    def stop(self):
        self.updateThread.exiting = True
        self.updateThread.terminate()


class TCPThread(QThread):
    def __init__(self, ports, parent=None):
        self.running = True
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.master_printer_name = '127.0.0.1'
        self.master_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.master_printer_port = int(parser.get('server_ports', 'master_udp'))
        self.messages_dict = {'get_my_ip': parser.get('server_strings', 'ask_for_my_ip'),
                              'get_my_port': parser.get('server_strings', 'ask_for_my_port'),
                              'get_client_hostname': parser.get('server_strings', 'ask_clients_hostname'),
                              'goodbye': parser.get('server_strings', 'goodbye_message'),
                              'request_message': parser.get('server_strings', 'request_message'),
                              'not_authorized': parser.get('server_strings', 'not_authorized'),
                              'not_authorized_log': parser.get('server_strings', 'not_authorized_log')}
        class_day = parser.get('class_settings', 'ClassDay')
        class_hours = parser.get('class_settings', 'ClassHours')
        exam_part = parser.get('class_settings', 'ExamPart')
        self.exam = {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part,
                     'server_type': 'TCP'}
        self.ports = ports
        super(TCPThread, self).__init__(parent)

    def run(self):
        servers_standard_format('TCP')
        server_ports = self.ports
        sock_lst = []
        host = ''
        backlog = 5
        buf_size = 1024
        my_messages = self.messages_dict
        connections_counter = 0
        try:
            for item in server_ports:
                sock_lst.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                sock_lst[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_lst[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock_lst[-1].bind((host, item))
                sock_lst[-1].listen(backlog)
        except socket.error, (value, message):
            if sock_lst[-1]:
                sock_lst[-1].close()
                # sock_lst = sock_lst[:-1]
            # print 'Could not open socket: ' + message
            sys.exit(1)
        while self.running:
            read, write, error = select.select(sock_lst, [], [])
            for r in read:
                for server_socket in sock_lst:
                    if r == server_socket:
                        connection_socket, client_address = server_socket.accept()
                        reg_id_received = connection_socket.recv(buf_size)
                        connections_counter += 1
                        if len(reg_id_received) == 0:
                            connection_socket.close()
                        else:
                            get_my_ip_from_client = my_messages['get_my_ip']
                            connection_socket.send(get_my_ip_from_client)
                            server_ip = connection_socket.recv(buf_size)
                            get_my_port_from_client = my_messages['get_my_port']
                            connection_socket.send(get_my_port_from_client)
                            server_port = connection_socket.recv(buf_size)
                            get_client_hostname = my_messages['get_client_hostname']
                            connection_socket.send(get_client_hostname)
                            client_hostname = connection_socket.recv(buf_size)
                            if expected_client(client_address[0], server_port, 'TCP'):
                                connection_socket.send(my_messages['request_message'])
                                client_message = connection_socket.recv(buf_size)
                                messages = server_effect_and_message(client_address[1], 'TCP', client_message)
                                connection_socket.send(messages['effected'])
                                connection_socket.send(messages['to_send'])
                                connection_socket.close()
                            else:
                                connection_socket.send(my_messages['not_authorized'])
                            server_client_conversation = [str(connections_counter), reg_id_received,
                                                          client_address[0], str(client_address[1]), server_ip,
                                                          server_port, client_hostname, ' ',
                                                          my_messages['not_authorized_log']]
                            format_log = servers_standard_format('TCP', server_client_conversation)
                            write_log(self.exam, format_log)
                            master_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            master_client_socket.sendto(format_log[9:],
                                                        (self.master_printer_name, self.master_printer_port))

    def stop(self):
        self.running = False
        self.socket.shutdown()


class UDP(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.srv = {}
        parser = SafeConfigParser()
        parser.read('settings.ini')
        start_port = int(parser.get('server_ports', 'udp_start'))
        end_port = int(parser.get('server_ports', 'udp_end'))
        self.master_printer_port = int(parser.get('server_ports', 'master_udp'))
        class_day = parser.get('class_settings', 'ClassDay')
        class_hours = parser.get('class_settings', 'ClassHours')
        exam_part = parser.get('class_settings', 'ExamPart')
        exam = {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part,
                'server_type': 'UDP'}
        clear_log(exam)
        write_log(exam, servers_standard_format('UDP'))
        server_ports = []
        if end_port < start_port:
            swap = end_port
            end_port = start_port
            start_port = swap
        for i in range(end_port - start_port + 1):
            server_ports.append(start_port + i)
        self.updateThread = UDPThread(server_ports)
        self.setup_update_thread()

    def setup_update_thread(self):
        if not self.updateThread.isRunning():
            self.updateThread.start()

    def stop(self):
        self.updateThread.exiting = True
        self.updateThread.terminate()


class UDPThread(QThread):
    def __init__(self, ports, parent=None):
        self .running = True
        parser = SafeConfigParser()
        parser.read('settings.ini')
        self.master_printer_name = '127.0.0.1'
        self.master_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.master_printer_port = int(parser.get('server_ports', 'master_udp'))
        self.messages_dict = {'get_my_ip': parser.get('server_strings', 'ask_for_my_ip'),
                              'get_my_port': parser.get('server_strings', 'ask_for_my_port'),
                              'get_client_hostname': parser.get('server_strings', 'ask_clients_hostname'),
                              'goodbye': parser.get('server_strings', 'goodbye_message'),
                              'request_message': parser.get('server_strings', 'request_message')}
        class_day = parser.get('class_settings', 'ClassDay')
        class_hours = parser.get('class_settings', 'ClassHours')
        exam_part = parser.get('class_settings', 'ExamPart')
        self.exam = {'class_day': class_day, 'class_hours': class_hours, 'exam_part': exam_part,
                     'server_type': 'UDP'}
        self.ports = ports
        super(UDPThread, self).__init__(parent)

    def run(self):
        server_ports = self.ports
        sock_lst = []
        host = ''
        buf_size = 1024
        my_messages = self.messages_dict
        connections_counter = 0
        try:
            for item in server_ports:
                sock_lst.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
                sock_lst[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_lst[-1].bind((host, item))
        except socket.error, (value, message):
            if sock_lst[-1]:
                sock_lst[-1].close()
                # sock_lst = sock_lst[:-1]
            # print 'Could not open socket: ' + message
            sys.exit(1)
        while self.running:
            read, write, error = select.select(sock_lst, [], [])
            for r in read:
                for server_socket in sock_lst:
                    if r == server_socket:
                        reg_id_received, client_address = server_socket.recvfrom(buf_size)
                        connections_counter += 1
                        get_my_ip_from_client = my_messages['get_my_ip']
                        server_socket.sendto(get_my_ip_from_client, client_address)
                        server_ip = server_socket.recvfrom(buf_size)
                        get_my_port_from_client = my_messages['get_my_port']
                        server_socket.sendto(get_my_port_from_client, client_address)
                        server_port = server_socket.recvfrom(buf_size)
                        get_client_hostname = my_messages['get_client_hostname']
                        server_socket.sendto(get_client_hostname, client_address)
                        client_hostname = server_socket.recvfrom(buf_size)
                        server_socket.sendto(my_messages['request_message'], client_address)
                        client_message = server_socket.recvfrom(buf_size)
                        server_socket.sendto(client_message[0].upper(), client_address)
                        server_socket.sendto(my_messages['goodbye'], client_address)
                        server_client_conversation = [str(connections_counter), reg_id_received,
                                                      client_address[0], str(client_address[1]), server_ip[0],
                                                      str(server_port[0]), client_hostname[0], client_message[0],
                                                      client_message[0].upper()]
                        format_log = servers_standard_format('UDP', server_client_conversation)
                        write_log(self.exam, format_log)
                        master_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        master_client_socket.sendto(format_log[8:],
                                                    (self.master_printer_name, self.master_printer_port))

    def stop(self):
        self.running = False
        self.socket.shutdown()
