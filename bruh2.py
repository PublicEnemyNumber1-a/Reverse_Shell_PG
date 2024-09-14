import socket
import struct
import cv2
import numpy as np

def start_server(host_ip, host_port, window_size=(1000, 600)):
    know = """
    Starts a server that listens for incoming connections and displays the received video stream.

    :param server_ip: IP address to bind the server to. Default is '0.0.0.0' (all interfaces).
    :param server_port: Port number to bind the server to. Default is 8080.
    """
    print(know)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, host_port))
    server_socket.listen(1)
    
    print("Server listening on {}:{}".format(host_ip, host_port))
    
    conn, addr = server_socket.accept()
    print("Connected to", addr)
    
    try:
        while True:
            # Receive the size of the data
            data_size = struct.unpack("L", conn.recv(struct.calcsize("L")))[0]
            # Receive the actual data
            data = b""
            while len(data) < data_size:
                packet = conn.recv(data_size - len(data))
                if not packet:
                    break
                data += packet
            
            # Convert the received data to an image
            nparr = np.frombuffer(data, np.uint8)
            screen_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if screen_np is None:
                print("Failed to decode image")
                continue
            
            # Convert the image from RGB to BGR
            screen_np = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            
            # Resize the image
            resized_screen = cv2.resize(screen_np, window_size)
            
            # Display the resized image
            cv2.imshow("Screen", resized_screen)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        conn.close()
        server_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_server('0.0.0.0', 8080)
