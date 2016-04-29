from ConfigParser import SafeConfigParser
from PySide.QtCore import Slot
from PySide.QtGui import QWidget, QVBoxLayout, QComboBox, QLabel, QGridLayout, QPushButton, QLineEdit
from parser import Parser

__author__ = 'lazToum'


class ClientSettings(QWidget):
    def __init__(self):
        self.parser1 = Parser()
        self.current = self.parser1.get_client_ipz()
        self.parser = SafeConfigParser()
        self.parser.read('settings.ini')
        ipz = self.parser1.get_client_ipz()
        QWidget.__init__(self)
        server_ports = self.parser1.get_server_ports()
        self.layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.alpha_input = QLineEdit(ipz[0])
        self.alpha_tcp_port = QComboBox(self)
        self.alpha_udp_port = QComboBox(self)
        self.save_alpha_button = QPushButton('&Save')
        self.save_alpha_button.clicked.connect(self.save_alpha)
        alpha = {'input': self.alpha_input, 'tcp_port': self.alpha_tcp_port, 'udp_port': self.alpha_udp_port,
                 'save': self.save_alpha_button}
        self.bravo_input = QLineEdit(ipz[1])
        self.bravo_tcp_port = QComboBox(self)
        self.bravo_udp_port = QComboBox(self)
        self.save_bravo_button = QPushButton('&Save')
        self.save_bravo_button.clicked.connect(self.save_bravo)
        bravo = {'input': self.bravo_input, 'tcp_port': self.bravo_tcp_port, 'udp_port': self.bravo_udp_port,
                 'save': self.save_bravo_button}
        self.charlie_input = QLineEdit(ipz[2])
        self.charlie_tcp_port = QComboBox(self)
        self.charlie_udp_port = QComboBox(self)
        self.save_charlie_button = QPushButton('&Save')
        self.save_charlie_button.clicked.connect(self.save_charlie)
        charlie = {'input': self.charlie_input, 'tcp_port': self.charlie_tcp_port, 'udp_port': self.charlie_udp_port,
                   'save': self.save_charlie_button}
        self.delta_input = QLineEdit(ipz[3])
        self.delta_tcp_port = QComboBox(self)
        self.delta_udp_port = QComboBox(self)
        self.save_delta_button = QPushButton('&Save')
        self.save_delta_button.clicked.connect(self.save_delta)
        delta = {'input': self.delta_input, 'tcp_port': self.delta_tcp_port, 'udp_port': self.delta_udp_port,
                 'save': self.save_delta_button}
        self.echo_input = QLineEdit(ipz[4])
        self.echo_tcp_port = QComboBox(self)
        self.echo_udp_port = QComboBox(self)
        self.save_echo_button = QPushButton('&Save')
        self.save_echo_button.clicked.connect(self.save_echo)
        echo = {'input': self.echo_input, 'tcp_port': self.echo_tcp_port, 'udp_port': self.echo_udp_port,
                'save': self.save_echo_button}
        self.foxtrot_input = QLineEdit(ipz[5])
        self.foxtrot_tcp_port = QComboBox(self)
        self.foxtrot_udp_port = QComboBox(self)
        self.save_foxtrot_button = QPushButton('&Save')
        self.save_foxtrot_button.clicked.connect(self.save_foxtrot)
        foxtrot = {'input': self.foxtrot_input, 'tcp_port': self.foxtrot_tcp_port, 'udp_port': self.foxtrot_udp_port,
                   'save': self.save_foxtrot_button}
        self.golf_input = QLineEdit(ipz[6])
        self.golf_tcp_port = QComboBox(self)
        self.golf_udp_port = QComboBox(self)
        self.save_golf_button = QPushButton('&Save')
        self.save_golf_button.clicked.connect(self.save_golf)
        golf = {'input': self.golf_input, 'tcp_port': self.golf_tcp_port, 'udp_port': self.golf_udp_port,
                'save': self.save_golf_button}
        self.hotel_input = QLineEdit(ipz[7])
        self.hotel_tcp_port = QComboBox(self)
        self.hotel_udp_port = QComboBox(self)
        self.save_hotel_button = QPushButton('&Save')
        self.save_hotel_button.clicked.connect(self.save_hotel)
        hotel = {'input': self.hotel_input, 'tcp_port': self.hotel_tcp_port, 'udp_port': self.hotel_udp_port,
                 'save': self.save_hotel_button}
        self.india_input = QLineEdit(ipz[8])
        self.india_tcp_port = QComboBox(self)
        self.india_udp_port = QComboBox(self)
        self.save_india_button = QPushButton('&Save')
        self.save_india_button.clicked.connect(self.save_india)
        india = {'input': self.india_input, 'tcp_port': self.india_tcp_port, 'udp_port': self.india_udp_port,
                 'save': self.save_india_button}
        self.juliet_input = QLineEdit(ipz[9])
        self.juliet_tcp_port = QComboBox(self)
        self.juliet_udp_port = QComboBox(self)
        self.save_juliet_button = QPushButton('&Save')
        self.save_juliet_button.clicked.connect(self.save_juliet)
        juliet = {'input': self.juliet_input, 'tcp_port': self.juliet_tcp_port, 'udp_port': self.juliet_udp_port,
                  'save': self.save_juliet_button}
        self.clients = {0: alpha, 1: bravo, 2: charlie, 3: delta, 4: echo, 5: foxtrot, 6: golf, 7: hotel, 8: india,
                        9: juliet}
        self.tcp_ports = ['Any'] + server_ports['TCP']
        self.udp_ports = ['Any'] + server_ports['UDP']
        j = 0
        for ipidx in ipz:
            client_ip_label = QLabel('Client IP:')
            grid_layout.addWidget(client_ip_label, j, 0)
            grid_layout.addWidget(self.clients[j]['input'], j, 1)
            client_tcp_port_label = QLabel('Connect to TCP Port:')
            grid_layout.addWidget(client_tcp_port_label, j, 2)
            self.clients[j]['tcp_port'].addItems(['Any'] + server_ports['TCP'])
            grid_layout.addWidget(self.clients[j]['tcp_port'], j, 3)
            client_udp_port_label = QLabel('Connect to UDP Port:')
            grid_layout.addWidget(client_udp_port_label, j, 4)
            self.clients[j]['udp_port'].addItems(['Any'] + server_ports['UDP'])
            grid_layout.addWidget(self.clients[j]['udp_port'], j, 5)
            grid_layout.addWidget(self.clients[j]['save'], j, 6)
            j += 1

        self.layout.addLayout(grid_layout)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    @Slot()
    def save_alpha(self):
        self.save_general(self.alpha_input.text(), self.alpha_tcp_port.currentIndex(),
                          self.alpha_udp_port.currentIndex(), 9)

    @Slot()
    def save_bravo(self):
        self.save_general(self.bravo_input.text(), self.bravo_tcp_port.currentIndex(),
                          self.bravo_udp_port.currentIndex(), 9)

    @Slot()
    def save_charlie(self):
        self.save_general(self.charlie_input.text(), self.charlie_tcp_port.currentIndex(),
                          self.charlie_udp_port.currentIndex(), 9)

    @Slot()
    def save_delta(self):
        self.save_general(self.delta_input.text(), self.delta_tcp_port.currentIndex(),
                          self.delta_udp_port.currentIndex(), 9)

    @Slot()
    def save_echo(self):
        self.save_general(self.echo_input.text(), self.echo_tcp_port.currentIndex(), self.echo_udp_port.currentIndex(),
                          9)

    @Slot()
    def save_foxtrot(self):
        self.save_general(self.foxtrot_input.text(), self.foxtrot_tcp_port.currentIndex(),
                          self.foxtrot_udp_port.currentIndex(), 9)

    @Slot()
    def save_golf(self):
        self.save_general(self.golf_input.text(), self.golf_tcp_port.currentIndex(), self.golf_udp_port.currentIndex(),
                          9)

    @Slot()
    def save_hotel(self):
        self.save_general(self.hotel_input.text(), self.hotel_tcp_port.currentIndex(),
                          self.hotel_udp_port.currentIndex(), 9)

    @Slot()
    def save_india(self):
        self.save_general(self.india_input.text(), self.india_tcp_port.currentIndex(),
                          self.india_udp_port.currentIndex(), 9)

    @Slot()
    def save_juliet(self):
        self.save_general(self.juliet_input.text(), self.juliet_tcp_port.currentIndex(),
                          self.juliet_udp_port.currentIndex(), 9)

    def save_general(self, client_name, client_tcp_port_index, client_udp_port_index, current_index):
        self.parser1.update_client(client_name, self.tcp_ports[client_tcp_port_index],
                                   self.udp_ports[client_udp_port_index])
        # print client_name + self.tcp_ports[client_tcp_port_index] + self.udp_ports[client_udp_port_index]
        # client_current_tcp_message = ''
        # client_current_udp_message = ''
        # client_current_effect = ''
        # client_current_ctrl_chars = ''
        # client_current_tcp_port = ''
        # client_current_udp_port = ''
        # client_current_tcp_port_restriction = ''
        # client_current_udp_port_restriction = ''
        # if self.parser.has_option('Client_TCP_Settings', self.current[current_index]):
        #     client_current_tcp_message = self.parser.get('Client_TCP_Settings', self.current[current_index])
        #     client_current_udp_message = self.parser.get('Client_UDP_Settings', self.current[current_index])
        #     client_current_effect = self.parser.get('Client_Effects', self.current[current_index])
        #     client_current_ctrl_chars = self.parser.get('Client_CTRL_Chars', self.current[current_index])
        #     client_current_tcp_port = self.parser.get('Server_Client_TCP_Ports', self.current[current_index])
        #     client_current_udp_port = self.parser.get('Server_Client_UDP_Ports', self.current[current_index])
        #     client_current_tcp_port_restriction =
        # self.parser.get('TCP_Ports_restriction', self.current[current_index])
        #     client_current_udp_port_restriction =
        #  self.parser.get('UDP_Ports_restriction', self.current[current_index])
        # else:
        #     if not self.parser.has_option('Client_TCP_Settings', client_name):
        #         self.parser.set('Client_TCP_Settings',
        #  client_name, self.parser.get('Client_TCP_Settings', self.current[current_index - 1]))
        #         self.parser.set('Client_UDP_Settings',
        #  client_name, self.parser.get('Client_UDP_Settings', self.current[current_index - 1]))
        #         self.parser.set('Client_Effects', client_name, '0')
        #         self.parser.set('Client_CTRL_Chars', client_name, '1')
        #         self.parser.set('Server_Client_TCP_Ports',
        #  client_name, self.parser.get('Server_Client_TCP_Ports', self.current[current_index - 1]))
        #         self.parser.set('Server_Client_UDP_Ports',
        #  client_name, self.parser.get('Server_Client_UDP_Ports', self.current[current_index - 1]))
        #         self.parser.set('TCP_Ports_restriction', client_name, '1')
        #         self.parser.set('UDP_Ports_restriction',client_name, '1')
        #     else:
        #         client_current_tcp_message = self.parser.get('Client_TCP_Settings', client_name)
        #         client_current_udp_message = self.parser.get('Client_UDP_Settings', client_name)
        #         client_current_effect = self.parser.get('Client_Effects', client_name)
        #         client_current_ctrl_chars = self.parser.get('Client_CTRL_Chars', client_name)
        #         client_current_tcp_port = self.parser.get('Server_Client_TCP_Ports', client_name)
        #         client_current_udp_port = self.parser.get('Server_Client_UDP_Ports', client_name)
        #         client_current_tcp_port_restriction = self.parser.get('TCP_Ports_restriction', client_name)
        #         client_current_udp_port_restriction = self.parser.get('UDP_Ports_restriction', client_name)
        # if client_name != self.current[current_index]:
        #     self.parser.remove_option('Client_TCP_Settings', self.current[current_index])
        #     self.parser.remove_option('Client_UDP_Settings', self.current[current_index])
        #     self.parser.remove_option('Client_Effects', self.current[current_index])
        #     self.parser.remove_option('Client_CTRL_Chars', self.current[current_index])
        #     self.parser.remove_option('Server_Client_TCP_Ports', self.current[current_index])
        #     self.parser.remove_option('Server_Client_UDP_Ports', self.current[current_index])
        #     self.parser.remove_option('TCP_Ports_restriction', self.current[current_index])
        #     self.parser.remove_option('UDP_Ports_restriction', self.current[current_index])
        #     self.parser.set('Client_TCP_Settings', client_name, client_current_tcp_message)
        #     self.parser.set('Client_UDP_Settings', client_name, client_current_udp_message)
        #     self.parser.set('Client_Effects', client_name, client_current_effect)
        #     self.parser.set('Client_CTRL_Chars', client_name, client_current_ctrl_chars)
        #     self.parser.set('Server_Client_TCP_Ports', client_name, client_current_tcp_port)
        #     self.parser.set('Server_Client_UDP_Ports', client_name, client_current_udp_port)
        #     self.parser.set('TCP_Ports_restriction', client_name, client_current_tcp_port_restriction)
        #     self.parser.set('UDP_Ports_restriction', client_name, client_current_udp_port_restriction)
        # if client_tcp_port_index == 0:
        #     self.parser.set('TCP_Ports_restriction', client_name, '1')
        # else:
        #     self.parser.set('TCP_Ports_restriction', client_name, '0')
        #     self.parser.set('Server_Client_TCP_Ports', client_name, str(self.tcp_ports[client_tcp_port_index]))
        # if client_udp_port_index == 0:
        #     self.parser.set('UDP_Ports_restriction', client_name, '1')
        # else:
        #     self.parser.set('UDP_Ports_restriction', client_name, '0')
        #     self.parser.set('Server_Client_UDP_Ports', client_name, str(self.udp_ports[client_udp_port_index]))
        # with open('settings.ini', 'wb') as configfile:
        #     self.parser.write(configfile)
        # self.clear_appended_clients()

    def clear_appended_clients(self):
        window_clients = [str(self.alpha_input.text()), str(self.bravo_input.text()), str(self.charlie_input.text()),
                          str(self.delta_input.text()), str(self.echo_input.text()), str(self.foxtrot_input.text()),
                          str(self.golf_input.text()), str(self.hotel_input.text()), str(self.india_input.text()),
                          str(self.juliet_input.text())]
        ini_records = self.parser1.get_client_ipz()
        print window_clients
        print ini_records
        # self.parser1.update_ipz(window_clients)
        # ini_clients = []
        # for i in ini_records:
        #     ini_clients.append(i)
        # for i in ini_records:
        #     if i in window_clients:
        #         pass
        #     else:
        #         self.parser.remove_option('Client_TCP_Settings', i)
        #         self.parser.remove_option('Client_UDP_Settings', i)
        #         self.parser.remove_option('Client_Effects', i)
        #         self.parser.remove_option('Client_CTRL_Chars', i)
        #         self.parser.remove_option('Server_Client_TCP_Ports', i)
        #         self.parser.remove_option('Server_Client_UDP_Ports', i)
        #         self.parser.remove_option('TCP_Ports_restriction', i)
        #         self.parser.remove_option('UDP_Ports_restriction', i)

    def run(self):
        self.show()
