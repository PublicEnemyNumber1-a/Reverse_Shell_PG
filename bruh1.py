import socket
import cv2
import pickle
import struct

def start_streaming_server(server_ip='0.0.0.0', server_port=8080):
    know = """
    Starts a server that listens for incoming connections and displays the received video stream.

    :param server_ip: IP address to bind the server to. Default is '0.0.0.0' (all interfaces).
    :param server_port: Port number to bind the server to. Default is 8080.
    """
    print(know)
    # Create socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print("[INFO] Server listening on port", server_port)

    # Accept a connection
    conn, addr = server_socket.accept()
    print("[INFO] Connection from", addr)

    try:
        while True:
            # Receive data size
            data_size = struct.unpack("L", conn.recv(struct.calcsize("L")))[0]
            data = b""

            # Receive data
            while len(data) < data_size:
                packet = conn.recv(data_size - len(data))
                if not packet:
                    break
                data += packet

            # Deserialize the frame
            frame = pickle.loads(data)

            # Display the frame
            cv2.imshow("Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Cleanup resources
        cv2.destroyAllWindows()
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_streaming_server(server_ip='0.0.0.0', server_port=8080)
