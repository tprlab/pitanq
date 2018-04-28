import os
import socket
import fcntl
import struct


ADDR_FILE = "/home/pi/pitanq/conf/host_hist.txt"


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])



class ConnCtrl:
    addr_list = set()
    def __init__(self):
        if os.path.isfile(ADDR_FILE):
            with open(ADDR_FILE) as f:
                lines = f.readlines()   
                self.addr_list = set(lines)
        addr = get_ip_address("wlan0")
        self.addr_list.add(addr)



            
if __name__ == '__main__':    
    c = ConnCtrl()
    print c.addr_list