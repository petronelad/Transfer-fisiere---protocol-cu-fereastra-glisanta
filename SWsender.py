import socket
import packetS


TIMER = 0.5
PACKET_SIZE = 200
WINDOW_SIZE = 8


'''
        create_buffer()
    all_packets = buffer with packets
    id_packet_in_buffer = number of packets in buffer
    Opening file with the text to send, creating packets and adding them in a buffer
'''
def create_buffer(file_to_send):
    try:
        file = open(file_to_send, 'rb')
    except IOError:
        print("The file can't be opened")
        return
    all_packets = []
    id_packet_in_buffer = 0
    while True:
        packet = packetS.Packet()
        packet.data = file.read(PACKET_SIZE)
        if not packet.data:
            break
        id_packet_in_buffer += 1
        flag = packetS.State.ON_HOLD
        packet.create_packet(id_packet_in_buffer, flag)
        all_packets.append(packet)
    file.close()
    return all_packets


'''
    send() - creates socket, sends packets, waits response 
     
    AF_INET represents  the address families, used for the first argument
    to the socket().
    SOCK_DGRAM is a cst that represents  the socket type, used for the 2nd
    argument to socket().
'''
def send(file_to_send):
    buffer = create_buffer(file_to_send)
    socket_for_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # socket.bind(address)
    # Bind the socket to address. The socket must not already be bound.
    # (The format of address depends on the address family — see above.)
    # Raises an auditing event socket.bind with arguments self, address.
    number_elem_in_win = 0
    
    for packet in buffer:
        if packet.flag == packetS.State.ON_HOLD:
            packet.send_packet(socket_for_send)
    socket_for_send.close()


if __name__ == '__main__':
    send("file_to_send.txt")

