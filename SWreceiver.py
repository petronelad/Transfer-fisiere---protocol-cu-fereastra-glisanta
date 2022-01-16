import socket
from struct import pack
import packetS

'''
    receive() - receives packets, 
    recvfrom return a pair(bytes, address) -> data received and address of the socket sender
'''

#primesc pachetul si trimit raspuns

#  def receive_packet( socket):
#         #functia apelata in receive din SWreceiver
#         #am luat datale primite si am refacut pachetul
#         data_and_id_in_bytes, source_address =  socket.recvfrom(4096)
#         self.id_packet = int.from_bytes(data_and_id_in_bytes[0:4], byteorder = 'little', signed = True)
#         self.data = data_and_id_in_bytes[4:]


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

        # packet.receive_packet(socket_received)
        data_and_id_in_bytes, source_address =  socket.recvfrom(4096)

        packet.id_packet = int.from_bytes(data_and_id_in_bytes[0:4], byteorder = 'little', signed = True)
        packet.data = data_and_id_in_bytes[4:]
        if not packet.data:
            break
        id_packet_in_buffer += 1
        packet.flag = packetS.State.RECEIVED
        all_packets.append(packet)
        print(packet.data)
        file.write(packet.data)
    file.close()
    socket_received.close()


if __name__ == '__main__':

    receive("file_received")

