import socket
import _thread
import packetS
import time


WAITING_TIME = 0.2
STOP_TIME = 1
TIMER_STOP = -1
PACKET_SIZE = 256
WINDOW_SIZE = 8

start_time = TIMER_STOP
my_thread = _thread.allocate_lock()
id_first_elem_in_window = 0

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
        packet.data = file.read(PACKET_SIZE)
        if not packet.data:
            break
        packet.create_packet(no_packet_in_buffer, packetS.State.ON_HOLD)
        all_packets.append(packet)
        no_packet_in_buffer += 1

    file.close()
    return all_packets, no_packet_in_buffer


'''
    send() - creates socket, sends packets, waits response 

    AF_INET represents  the address families, used for the first argument
    to the socket().
    SOCK_DGRAM is a cst that represents  the socket type, used for the 2nd
    argument to socket().'''

def send_and_receive_ack(file_to_send, socket_for_send):
    global id_first_elem_in_window, start_time
    id_next_elem_to_send = 0
    id_first_elem_in_window = 0
    buffer, number_packets = create_buffer(file_to_send)


    print("to send")
    var = 3
    _thread.start_new_thread(receive, (socket_for_send,))
    while id_first_elem_in_window < number_packets:
        # lock.acquire(waitflag=1, timeout=- 1) -> lock unconditionally, if necessary waiting until it is released by another thread
        # lock.release() -> free the lock. The lock must have been acquired earlier, but not necessarily by the same thread.
        my_thread.acquire()
        while id_first_elem_in_window + WINDOW_SIZE > id_next_elem_to_send:
            if buffer[id_next_elem_to_send].flag == packetS.State.ON_HOLD:
                buffer[id_next_elem_to_send].flag = packetS.State.SEND
                # if id_next_elem_to_send==var:
                #     id_next_elem_to_send=4
                #     var=0
                print(buffer[id_next_elem_to_send].id_packet.to_bytes(4, byteorder='little', signed=True) + buffer[
                    id_next_elem_to_send].flag.value.to_bytes(4, byteorder='little', signed=True) + \
                      buffer[id_next_elem_to_send].data)
                socket_for_send.sendto(buffer[id_next_elem_to_send].id_packet.to_bytes(4, byteorder='little', signed=True) \
                    + buffer[id_next_elem_to_send].flag.value.to_bytes(4, byteorder='little', signed=True) + buffer[
                    id_next_elem_to_send].data, packetS.DESTINATION_ADDRESS)
                # print(buffer[id_next_elem_to_send].data)
                id_next_elem_to_send += 1
        start_time = time.time()
        # we need a while waiting for timeout or an akn
        while time.time() - start_time < STOP_TIME :
            my_thread.release()
            print("waiting")
            time.sleep(WAITING_TIME)
            my_thread.acquire()

        # if the time is out and we didn t receive an ackowledge, we put the beginning of window on this element
        if time.time() - start_time >= STOP_TIME:
            print("timeout\n")
            start_time = TIMER_STOP
            id_next_elem_to_send = id_first_elem_in_window

            my_thread.release()
    socket_for_send.sendto(id_next_elem_to_send.to_bytes(4, byteorder='little', signed=True) + var.to_bytes(4, byteorder='little', signed=True) +b''
                           , packetS.DESTINATION_ADDRESS)


def receive(socket_for_send):
    global id_first_elem_in_window, start_time
    try:
        while True:
            try:
                print("+1+")
                # check what we receive
                packet, client_address = socket_for_send.recvfrom(512)
                # print(packet, client_address)

                # to see the id for received packet
                acknowledge = int.from_bytes(packet[0:4], byteorder='little', signed=True)
                print("it s sent the packet ", acknowledge)
                status = int.from_bytes(packet[4:], byteorder='little', signed=True)
                print("status ", status)
                # with each received packet, the window will be slide
                if acknowledge >= id_first_elem_in_window and status == 3:
                    my_thread.acquire()
                    id_first_elem_in_window = acknowledge + 1
                    start_time = TIMER_STOP
                    # the time is not out.We receive an ackowledge, the wind will be slide
                    print("sliding window")
                    my_thread.release()

            except OSError:

                print("------------it's over-----------")
                _thread.exit()
    except KeyboardInterrupt:
        print("keyboardinterrupt")


def send(file_to_send):
    # Bind the socket to address. The socket must not already be bound.
    # (The format of address depends on the address family — see above.)
    # Raises an auditing event socket.bind with arguments self, address.
    socket_for_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_for_send.bind(packetS.SOURCE_ADDRESS)
    send_and_receive_ack(file_to_send, socket_for_send)
    socket_for_send.close()


if __name__ == '__main__':
    send("file_to_send.txt")