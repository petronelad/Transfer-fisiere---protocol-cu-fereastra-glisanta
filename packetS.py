from enum import Enum
from sys import byteorder


class State(Enum):
        ON_HOLD = 1
        SEND = 2
        RECEIVED = 3
        UNKNOWN = 4


''' 
    packet structure
    ID_PACKET - packet number 
    FLAG - ON_HOLD, SEND, RECEIVED - packet state
    DATA - information to send
'''

SOURCE_ADDRESS = ('localhost', 8080)
DESTINATION_ADDRESS = ('localhost', 8081)

class Packet:
    def __init__(self):
        # self.id_packet = 1
        self.flag = 0
        self.data = b''


    def create_packet(self, id_packet, flag):
        self.id_packet = id_packet
        self.flag = flag


    def send_response(self):
        # print(self.id_packet.to_bytes(4, byteorder = 'little', signed = True) + State.RECEIVED.value.to_bytes(4, byteorder = 'little', signed = True))
        return self.id_packet.to_bytes(4, byteorder = 'little', signed = True) + State.RECEIVED.value.to_bytes(4, byteorder = 'little', signed = True)