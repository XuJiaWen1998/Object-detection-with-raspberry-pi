import cv2
import numpy as np
import socket
from threading import Thread
class remote_user():
    def __init__(self, IP='127.0.0.1', PORT=8000):
        # Set up the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(1)
        # Accept a client connection
        self.client_socket, self.client_address = self.server_socket.accept()

        
    def recvall(self, length):
        buf = b''
        while length:
            data = self.client_socket.recv(length)
            if not data: 
                return None
            buf += data
            length -= len(data)
        return buf
    
    def get_image(self):
        # Convert the received data back to an image
        length = self.recvall(16)
        stringData = self.recvall(int(length))
        data = np.fromstring(stringData, dtype='uint8')
        
        # Display the received image
        self.image = cv2.imdecode(data,1)
        self.client_socket.send("Image Received".encode())

    def get_packet(self):
        length = self.recvall(16)
        self.packet = self.recvall(int(length))
        self.client_socket.send("Packet Received".encode())

    
    def print_packet(self):
        self.output = self.packet.decode()
        if len(self.output) != 0:
            print(self.output)

    def show_image(self):
        cv2.imshow('Smart Home', self.image)
        cv2.waitKey(1)

    def close_socket(self):
        # Close the connection
        self.client_socket.close()
        self.server_socket.close()

def run_remote_user(IP='127.0.0.1', PORT=8000):
    u = remote_user(IP, PORT)
    try:
        while True:
            u.get_image()
            u.show_image()
            u.get_packet()
            u.print_packet()
        
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Closing the socket.")
        u.close_socket()
    
if __name__ == '__main__':
    run_remote_user()