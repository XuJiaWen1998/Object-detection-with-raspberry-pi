import cv2
import numpy as np
import socket
from movement_detector import *

def run_remote_monitor(IP='127.0.0.1', PORT=8000):
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    # Create movement_detector
    try:
        m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
        while True:
            # Load the image
            image, messages = m.run(show=False)

            # Convert the image to a string
            
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            result, image_data = cv2.imencode('.jpg', image, encode_param)
            data = np.array(image_data)
            
            stringData = data.tostring()

            # Send the image data
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.sendall(image_data)
            
            packet = ''
            for message in messages:
                packet += message
                packet += '\n'
                print(message)

            client_socket.recv(4096).decode()

            # Send the message
            client_socket.send(str(len(packet)).ljust(16).encode())
            client_socket.sendall(packet.encode())

            client_socket.recv(4096)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Closing the socket.")

    # Close the connection
    client_socket.close()

if __name__ == '__main__':
    run_remote_monitor()