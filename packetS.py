from enum import Enum


class State(Enum):
        ON_HOLD = 1
        SEND = 2
        RECEIVED = 3


''' 
    packet structure
    ID_PACKET - packet number 
    SOURCE_ADDRESS
    DESTINATION_ADDRESS
    FLAG - ON_HOLD, SEND, RECEIVED - packet state
    DATA - information to send
'''

SOURCE_ADDRESS = ('localhost', 8080)
DESTINATION_ADDRESS = ('localhost', 8081)

class Packet:

    source_address = SOURCE_ADDRESS
    destination_address = DESTINATION_ADDRESS


    def __init__(self):
        id_packet = 1
        source_address = ('localhost', 8080)
        destination_address =  ('localhost', 8081)
        flag = 0
        data = b''


    def create_packet(self, id_packet, flag):
        self.id_packet = id_packet
        self.flag = flag


    def send_packet(self, socket):
        self.flag = State.SEND
        id_packet_in_bytes = self.id_packet.to_bytes(4, byteorder='little', signed=True)
        socket.sendto(self.data + id_packet_in_bytes, self.destination_address)


    def receive_packet(self, socket):
        #functia apelata in receive din SWreceiver
        #am luat datale primite si am refacut pachetul
        data_and_id_in_bytes, self.source_address =  socket.recvfrom(4096)
        self.id_packet = int.from_bytes(data_and_id_in_bytes[0:4], byteorder = 'little', signed = True)
        self.data = data_and_id_in_bytes[4:]


    def send_response(self):
        self.flag = State.RECEIVED





