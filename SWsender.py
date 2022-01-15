import socket
import threading
import packetS
import time


TIMER = 2
PACKET_SIZE = 200
WINDOW_SIZE = 8


'''
        create_buffer()
    all_packets = buffer with packets
    id_packet_in_buffer = number of packets in buffer
    Opening file with the text to send, creating packets and adding them in a buffer'''


def create_buffer(file_to_send):
    try:
        file = open(file_to_send, 'rb')
    except IOError:
        print("The file can't be opened")
        return
    all_packets = []
    no_packet_in_buffer = 0
    while True:
        packet = packetS.Packet()
        packet.data =file.read(PACKET_SIZE)
        if not packet.data:
            break
        no_packet_in_buffer += 1
        packet.create_packet(no_packet_in_buffer, packetS.State.ON_HOLD)
        all_packets.append(packet)
    file.close()
    return all_packets, no_packet_in_buffer


'''
    send() - creates socket, sends packets, waits response 
     
    AF_INET represents  the address families, used for the first argument
    to the socket().
    SOCK_DGRAM is a cst that represents  the socket type, used for the 2nd
    argument to socket().'''


def send(file_to_send):

    # Bind the socket to address. The socket must not already be bound.
    # (The format of address depends on the address family — see above.)
    # Raises an auditing event socket.bind with arguments self, address.

    socket_for_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_for_send.bind(packetS.SOURCE_ADDRESS)
    socket_for_send.settimeout(TIMER)

    print("to send")

    buffer, number_packets = create_buffer(file_to_send)
    

    start_time = time.time()
    
    number_elem_in_win = 0
    packet_index = 0

    # threading.start_new_thread()

    while True:
        try:
            new_packet, client_address = socket_for_send.recvfrom(packetS.DESTINATION_ADDRESS[1])


        except:
            break

    # while number_elem_in_win < WINDOW_SIZE:
    #     for packet in buffer:
    #         if packet.flag == 1:
    #             number_elem_in_win += 1
    #             if number_elem_in_win >= WINDOW_SIZE:
    #                 break
    #             packet.send_packet(socket_for_send)
    #             print(packet.data)

    for packet in buffer:
        if packet.flag == packetS.State.ON_HOLD and number_elem_in_win < WINDOW_SIZE:
            packet.flag = packetS.State.SEND
            id_packet_in_bytes = packet.id_packet.to_bytes(4, byteorder='little', signed=True)
            socket.sendto(packet.data + id_packet_in_bytes, packetS.DESTINATION_ADDRESS)
            print(packet.data)
    
    socket_for_send.close()


if __name__ == '__main__':
    send("file_to_send.txt")

