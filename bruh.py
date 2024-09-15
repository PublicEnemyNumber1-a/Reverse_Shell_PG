import socket
import pyaudio
import struct
import sys

# Setup audio configuration
chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 44100

# Setup socket server
server_ip = '0.0.0.0'
server_port = 8080

def receive_audio_from_client():
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

if __name__ == "__main__":
    receive_audio_from_client()
