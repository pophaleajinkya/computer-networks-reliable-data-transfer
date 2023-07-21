import utility
from main import RDTSocket
import sys

SERVER = str(sys.argv[1])
file = '../computer_networks_rdt_udp/download.txt'
PORT = int(sys.argv[2])
window_size = int(sys.argv[3])
server = RDTSocket(SERVER, PORT)
server.bind()
data_coll_list = []
ack_list = []

while True:
    data_collected, address = server.recvfrom(2048)
    # set up the connection and ready to receive
    if data_collected.PacketHeader.type == 0:
        server.accept(address, window_size)
        print("Receiver accepted the connection request from the sender...")
        # incoming data packet
    elif data_collected.PacketHeader.type == 2 and server.connection_status1:
        # verify  checksum
        if not utility.check_checksum(data_collected.data, data_collected.PacketHeader.checksum):
            server.sendACK(data_collected.PacketHeader.seq_num, address, -window_size)
            ack_list.append(0)
            print("error")
            continue
        # append the ACKs all-in-one
        ack_list.append(1)
        data_coll_list.append(data_collected.data)
        # check the sliding window
        # if packet not acknowledged, re-transmit it.
        if len(ack_list) > window_size and ack_list[len(ack_list) - window_size] == 0:
            server.sendACK(data_collected.PacketHeader.seq_num + 1, address, window_size * (-1))
            ack_list = ack_list[:window_size * (-1)]
            message_list = data_coll_list[:window_size * (-1)]
        else:
            server.sendACK(data_collected.PacketHeader.seq_num + 1, address, 1)
            print("-------------------")
            print(f"Sequence number is {data_collected.PacketHeader.seq_num}")
            print(f"Data from Client:\n {data_collected.data}")
            print(f"Client Address:{address}")
    # receive an end command
    elif data_collected.PacketHeader.type == 1 and server.connection_status1:
        # handle remaining packets in the buffer
        for i in range(len(ack_list) - window_size, len(ack_list) - 1):
            if len(ack_list) > window_size and ack_list[len(ack_list) - window_size] == 0:
                server.sendACK(data_collected.PacketHeader.seq_num + 1, address, window_size * (-1))
                ack_list = ack_list[:window_size * (-1)]
                message_list = data_coll_list[:window_size * (-1)]
                break
        server.sendACK(-1, address, 0)
        # write the data received into a download.txt
        with open(file, 'w') as f:
            for msg in data_coll_list:
                f.writelines(msg)
            f.close()
