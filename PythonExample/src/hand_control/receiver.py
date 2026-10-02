import socket
import time
import json
from src.hand_control.params import MAX_UDP_PACKET_SIZE,  WAIT_TIMEOUT

class UDPReceiver:

    def __init__(self, port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", port))
        self.sock.setblocking(False)

    def clear_buffer(self):
        while True:
            try:
                self.sock.recvfrom(MAX_UDP_PACKET_SIZE)
            except BlockingIOError:
                break

    def wait_for_sensor_data(self):
        """Wait for sensor data and return it as a list of integers."""

        self.clear_buffer()
        counter = 0
        

        while True:
            try:
                data, address = self.sock.recvfrom(MAX_UDP_PACKET_SIZE)

                message = json.loads(data.decode())
                sensor_data = [int(value) for value in message["values"]]

                if sensor_data:
                    return sensor_data

            except BlockingIOError:
                pass

            time.sleep(0.01)
            counter += 1

            if counter > WAIT_TIMEOUT:
                raise TimeoutError("Timeout waiting for sensor data.")
            