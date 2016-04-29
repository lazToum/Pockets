from ConfigParser import SafeConfigParser
from random import randint

__author__ = 'lazToum'


class Parser:
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read('settings.ini')

    def get_server_ports(self):
        master_port = self.parser.get('server_ports', 'first_tcp_start')
        tcp_start_port = int(self.parser.get('server_ports', 'first_tcp_start'))
        tcp_end_port = int(self.parser.get('server_ports', 'first_tcp_end'))
        tcp_server_ports = []
        udp_server_ports = []
        if tcp_end_port < tcp_start_port:
            swap = tcp_end_port
            tcp_end_port = tcp_start_port
            tcp_start_port = swap
        for i in range(tcp_end_port - tcp_start_port + 1):
            tcp_server_ports.append(str(tcp_start_port + i))
        udp_start_port = int(self.parser.get('server_ports', 'udp_start'))
        udp_end_port = int(self.parser.get('server_ports', 'udp_end'))
        if udp_end_port < udp_start_port:
            swap = udp_end_port
            udp_end_port = udp_start_port
            udp_start_port = swap
        for i in range(udp_end_port - udp_start_port + 1):
            udp_server_ports.append(str(udp_start_port + i))
        return {'TCP': tcp_server_ports, 'UDP': udp_server_ports, 'MasterUDP': master_port}

    def get_client_ipz(self):
        return self.parser.options('TCP_Ports_restriction')

    def ip_exists(self, ip):
        return self.parser.has_option('TCP_Ports_restriction', ip)

    def get_client_tcp_port(self, ip):
        return self.parser.get('Server_Client_TCP_Ports', ip)

    def get_client_udp_port(self, ip):
        return self.parser.get('Server_Client_UDP_Ports', ip)

    def tcp_ports_open(self, ip):
        return self.parser.get('TCP_Ports_restriction', ip) == '1'

    def udp_ports_open(self, ip):
        return self.parser.get('UDP_Ports_restriction', ip) == '1'

    def get_client_tcp_message(self, ip):
        return self.parser.get('Client_TCP_Settings', ip)

    def get_client_udp_message(self, ip):
        return self.parser.get('Client_UDP_Settings', ip)

    def update_client(self, ip, tcp_port, udp_port):
        if tcp_port == 'Any':
            self.parser.set('TCP_Ports_restriction', ip, '1')
        else:
            self.parser.set('TCP_Ports_restriction', ip, '0')
            self.parser.set('Server_Client_TCP_Ports', ip, tcp_port)
        if udp_port == 'Any':
            self.parser.set('UDP_Ports_restriction', ip, '1')
        else:
            self.parser.set('UDP_Ports_restriction', ip, '0')
            self.parser.set('Server_Client_UDP_Ports', ip, udp_port)
        if not self.ip_exists(ip):
            ipz = self.get_client_ipz()
            ip = ipz[randint(0, len(ipz) - 1)]
            self.parser.set('Client_TCP_Settings', self.parser.get('Client_TCP_Settings', ip))
            self.parser.set('Client_UDP_Settings', self.parser.get('Client_UDP_Settings', ip))
            self.parser.set('Client_Effects', '0')
            self.parser.set('Client_CTRL_Chars', '1')

    def update_ipz(self, ipz):
        ini_ipz = self.get_client_ipz()
        for i in ini_ipz:
            if i in ipz:
                pass
            else:
                self.parser.remove_option('Client_TCP_Settings', i)
                self.parser.remove_option('Client_UDP_Settings', i)
                self.parser.remove_option('Client_Effects', i)
                self.parser.remove_option('Client_CTRL_Chars', i)
                self.parser.remove_option('Server_Client_TCP_Ports', i)
                self.parser.remove_option('Server_Client_UDP_Ports', i)
                self.parser.remove_option('TCP_Ports_restriction', i)
                self.parser.remove_option('UDP_Ports_restriction', i)
