import struct
import socket

from .header import *


def decode_header(packet, offset):
    """Decode a navdata header."""
    header = dict(zip(('header', 'drone_state', 'seq_nr', 'vision_flag'), struct.unpack_from("IIII", packet, offset)))
    header['drone_state'] = {state_name: header['drone_state'] >> shift & 1 for shift, state_name in enumerate(DRONE_STATES)}
    return header, offset + struct.calcsize("IIII")


def decode_option(packet, offset):
    """Decode a navdata option."""
    id_nr, size = struct.unpack_from("HH", packet, offset)
    end_offset = offset + size
    data = packet[offset + struct.calcsize("HH"):end_offset]
    return id_nr, data, end_offset


def decode_navdata(packet):
    """Decode a navdata packet."""
    offset = 0
    header, offset = decode_header(packet, offset)
    data = {}
    while offset < len(packet):
        id_nr, id_data, offset = decode_option(packet, offset)
        data[id_nr] = id_data
    return header, data


class ARDroneNavdata:
    def __init__(self, ip=ARDRONE_IP, port=ARDRONE_NAVDATA_PORT):
        self.comwdg_interval = COMWDG_INTERVAL
        self.address = (ip, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', port))
        self.s.sendto("\x01\x00\x00\x00", self.address)
        self.s.setblocking(0)

    def pull(self):
        while True:
            try:
                data = self.s.recv(65535)
            except IOError:
                # we consumed every packet from the socket and
                # continue with the last one
                break
        return decode_navdata(data)

    __call__ = pull

    def close(self):
        self.s.close()

    __del__ = close
