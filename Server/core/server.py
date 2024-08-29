
import socket
import threading
from Server.handlers.request import handle_request

def start_server(host='localhost', port = 5555):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexion aceptada de {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    response = handle_request(request)
    client_socket.send(response.encode())
    client_socket.close()
