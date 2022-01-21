import socket
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
    expected_id_packet = 0
    packet = packetS.Packet()
    print("hi")
    while True:
        data_and_id_in_bytes, source_address = socket_received.recvfrom(512)
        packet.id_packet = int.from_bytes(data_and_id_in_bytes[0:4], byteorder='little', signed=True)
        packet.flag = packetS.State(int.from_bytes(data_and_id_in_bytes[4:8], byteorder='little', signed=True))
        packet.data = data_and_id_in_bytes[8:]
        if not packet.data:
            break
        print(packet.id_packet, expected_id_packet)
        print(packet.data)
        # file.write(packet.data)
        print("R: expected packet ", expected_id_packet, "\nR: received packet ", packet.id_packet)
        print("R: ack can be sent")
        # interface.text_box2.insert(END, "  R: expected packet " + str(expected_id_packet) + ", received packet " + str(
        #     packet.id_packet))

        # sending ack
        if expected_id_packet == packet.id_packet:
            # interface.GUI.text_box2.insert(END, "R: Packet:\n" + str(packet.data))
            packet.flag = packetS.State.RECEIVED
            socket_received.sendto(packet.send_response(), source_address)
            expected_id_packet += 1
        else:
            print("R: lost packet")
            #interface.GUI.text_box2.insert(END, "R: lost packet "+str(expected_id_packet))
            print(expected_id_packet.to_bytes(4, byteorder='little', signed=True) + \
                  packetS.State.UNKNOWN.value.to_bytes(4, byteorder='little', signed=True))
            socket_received.sendto(expected_id_packet.to_bytes(4, byteorder='little', signed=True) + \
                  packetS.State.UNKNOWN.value.to_bytes(4, byteorder='little', signed=True), source_address)
    file.close()


def receive(file_received):
    socket_received = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_received.bind(packetS.DESTINATION_ADDRESS)
    receive_packet_and_send_ack(file_received, socket_received)
    socket_received.close()


if __name__ == '__main__':
    receive("file_received.txt")