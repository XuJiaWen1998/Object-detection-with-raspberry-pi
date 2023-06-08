import cv2
import numpy as np
import socket
import time
from movement_detector import *

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8000))

# Create movement_detector
try:
    m = movement_detector(threshold=0.5, nms_threshold=0.2, objects=[])
    while True:
        # Load the image
        image = m.run(show=False)

        # Convert the image to a string
        
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, image_data = cv2.imencode('.jpg', image, encode_param)
        data = np.array(image_data)
        
        stringData = data.tostring()
        # Send the image data
        client_socket.send(str(len(stringData)).ljust(16).encode())
        client_socket.sendall(image_data)

except KeyboardInterrupt:
    print("Keyboard interrupt received. Closing the socket.")

# Close the connection
client_socket.close()