import sys
from main import RDTSocket

SERVER = str(sys.argv[1])
file = '../computer_networks_rdt_udp/alice.txt'
file_to_copy = '../computer_networks_rdt_udp/download.txt'
PORT = int(sys.argv[2])
window_size = int(sys.argv[3])

# place a connection request
client = RDTSocket(SERVER, PORT)
client.connect()
print('Sender has placed a connection request to the receiver')
start_pkt_from_server = client.recv(2048)
seq_num = start_pkt_from_server.PacketHeader.seq_num
print(f"ACK seq_num is {start_pkt_from_server.PacketHeader.seq_num}")

# prepare to send data
with open(file) as f:
    message = f.readlines()

# break the message into k packets
i = 0
while i < len(message):
    msg = message[i]
    client.sendto(msg, client.ADDR, seq_num)
    pkt_from_server = client.recv(2048)
    seq_num = pkt_from_server.PacketHeader.seq_num
    # Instruction from the receiver
    if pkt_from_server.PacketHeader.type == 3:
        print(f"ACK seq_num is {pkt_from_server.PacketHeader.seq_num}")
        i += pkt_from_server.data
        continue
    else:
        print("Error from server end")
        break

# close the connection after transfer of all packets
client.close()
pkt_from_server = client.recv(2048)
if pkt_from_server.PacketHeader.type == 3:
    print("Text file transferred to download.txt!!!")
    client.socket.close()
