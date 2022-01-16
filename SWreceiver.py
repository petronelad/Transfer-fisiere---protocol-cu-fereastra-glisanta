import socket
from struct import pack
import packetS

'''
    receive() - receives packets, 
    recvfrom return a pair(bytes, address) -> data received and address of the socket sender
'''


def receive_packet_and_send_ack(file_received, socket_received):
    try:
        file = open(file_received, 'wb')
    except IOError:
        print("The file can't be opened")
        return
    id_packet_in_buffer = 0
    all_packets = []
    packet = packetS.Packet()

    while True:

        # packet.receive_packet(socket_received)
        data_and_id_in_bytes, source_address = socket_received.recvfrom(1024)
        packet.id_packet = int.from_bytes(data_and_id_in_bytes[0:4], byteorder='little', signed=True)
        packet.flag = packetS.State(int.from_bytes(data_and_id_in_bytes[4:8], byteorder='little', signed=True))
        packet.data = data_and_id_in_bytes[4:]
        if not packet.data:
            break

        if id_packet_in_buffer == packet.id_packet:
            print("expected packet ", id_packet_in_buffer, "\nreceived packet ", packet.id_packet)
            print("ack can be sent")
            socket_received.sendto(packet.send_response(), source_address)
            packet.flag = packetS.State.RECEIVED
            id_packet_in_buffer += 1

            all_packets.append(packet)
            print(packet.data)
            file.write(packet.data)
        else:
            print("lost packet")
            print(
                id_packet_in_buffer.to_bytes(4, byteorder='little', signed=True) + packetS.State.UNKNOWN.value.to_bytes(
                    4, byteorder='little', signed=True))
            socket_received.sendto(
                id_packet_in_buffer.to_bytes(4, byteorder='little', signed=True) + packetS.State.UNKNOWN.value.to_bytes(
                    4, byteorder='little', signed=True), source_address)
    file.close()


def receive(file_received):
    socket_received = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_received.bind(packetS.DESTINATION_ADDRESS)
    receive_packet_and_send_ack(file_received, socket_received)
    socket_received.close()


if __name__ == '__main__':
    receive("file_received")