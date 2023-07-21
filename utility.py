import zlib
import socket
from queue import Queue

class PacketHeader:
    def __init__(self, type, seq_num, length, checksum):
        self.type = type
        self.seq_num = seq_num
        self.length = length
        self.checksum = checksum


class Packet:
    def __init__(self, header, data):
        self.PacketHeader = header
        self.data = data


class UnreliableSocket:
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ADDR = (ip, port)

    def bind(self):
        self.socket.bind(self.ADDR)

    def sendto(self, data, address, seq_num):
        pass

    def close(self):
        self.socket.close()


def makeAck(sqe_num, checksum, data):
    header = PacketHeader(3, sqe_num, 0, checksum)
    pkt = Packet(header, data)
    return pkt


def makeStart(sqe_num, checksum):
    header = PacketHeader(0, sqe_num, 0, checksum)
    pkt = Packet(header, "")
    return pkt


def makeEnd(sqe_num, checksum):
    header = PacketHeader(1, sqe_num, 0, checksum)
    pkt = Packet(header, "")
    return pkt


def getCheckSum(data):
    checksum = zlib.crc32(data.encode())
    return checksum


def check_checksum(data, checksum):
    return getCheckSum(data) == checksum

def clean_queue(queue):
    while not queue.empty():
        queue.get()
    return queue