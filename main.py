import pickle
import random as rand
from time import sleep

import utility
import socket


class RDTSocket(utility.UnreliableSocket):
    def __init__(self, ip, port):
        self.connection_status = 0
        self.connection_status1 = False    # flag to show connect status
        self.ADDR = (ip, port)          # address info
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #accept connection request from sender and send an ACK
    def accept(self, address, window_size):
        self.connection_status1 = True
        self.sendACK(0, address, window_size)

    #send a connection request to the receiver
    def connect(self):
        start_pkt = pickle.dumps(utility.makeStart(0, "10100101"))
        self.socket.sendto(start_pkt, self.ADDR)

    #send data to the receiver
    def sendto(self, data, address, seq_num):
        header = utility.PacketHeader(2, seq_num, len(data), utility.getCheckSum(data))
        data = utility.Packet(header, data)
        data = pickle.dumps(data)
        self.socket.sendto(data, address)

    #receive data from the sender
    def recvfrom(self, size):
        pkt, address = self.socket.recvfrom(size)
        pkt = pickle.loads(pkt)
        # Apply simulated failures
        if rand.random() < self.connection_status:
            initialize_series = rand.choice(["packet loss", "packet delay", "packet corruption"])
            # Apply the selected event
            match initialize_series:
                case "packet loss":
                     pkt.PacketHeader.seq_num = 0
                     pkt.PacketHeader.checksum = 0
                     pkt.PacketHeader.length = 0
                     pkt.data = 0
                case "packet delay":
                    sleep(500)
                case "packet corruption":
                    pkt.data = rand.randint(0, 100000)
            # Switch the data to the modified data
        return pkt, address

    def sendACK(self, seq_num, address, data):
        ack_pkt = pickle.dumps(utility.makeAck(seq_num, 000000000, data))
        self.socket.sendto(ack_pkt, address)

    def recv(self, size):
        pkt = self.socket.recv(size)
        return pickle.loads(pkt)

    def close(self):
        end_pkt = pickle.dumps(utility.makeEnd(10000, 000000000))
        self.socket.sendto(end_pkt, self.ADDR)



