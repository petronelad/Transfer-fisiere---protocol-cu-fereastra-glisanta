import socket
import packetS

'''
    receive() - receives packets, 
    recvfrom return a pair(bytes, address) -> data received and address of the socket sender
'''

#primesc pachetul si trimit raspuns

def receive(file_received):
    try:
        file = open(file_received, 'wb')
    except IOError:
        print("The file can't be opened")
        return
    id_packet_in_buffer = 0
    all_packets = []
    packet = packetS.Packet()
    socket_received = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_received.bind(packetS.DESTINATION_ADDRESS)
    while True:
        packet.receive_packet(socket_received)
        if not packet.data:
            break
        id_packet_in_buffer += 1
        packet.flag = packetS.State.RECEIVED
        all_packets.append(packet)
        file.write(packet.data)
    file.close()
    socket_received.close()


if __name__ == '__main__':

    receive("file_received")

