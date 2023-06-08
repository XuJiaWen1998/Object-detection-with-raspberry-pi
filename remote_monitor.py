import cv2
import numpy as np
import socket
from movement_detector import *

class remote_monitor():
    def __init__(self, IP='127.0.0.1', PORT=8000):
        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])


    def run(self):
        # Load the image
        image, messages = self.m.run(show=False)

        # Convert the image to a string
        
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, image_data = cv2.imencode('.jpg', image, encode_param)
        data = np.array(image_data)
        
        stringData = data.tostring()

        # Send the image data
        self.client_socket.send(str(len(stringData)).ljust(16).encode())
        self.client_socket.sendall(image_data)
        
        packet = ''
        for message in messages:
            packet += message
            packet += '\n'
            print(message)

        self.client_socket.recv(4096).decode()

        # Send the message
        self.client_socket.send(str(len(packet)).ljust(16).encode())
        self.client_socket.sendall(packet.encode())

        self.client_socket.recv(4096)
        return image, messages

    def run_remote_monitor_loop(self):
        try:
            while True:
                 self.run()
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Closing the socket.")
        # Close the connection
        self.client_socket.close()

if __name__ == '__main__':
    monitor = remote_monitor()
    monitor.run_remote_monitor_loop()