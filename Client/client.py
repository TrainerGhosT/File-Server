import socket

def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

def upload_file(filename, content):
    request = f"UPLOAD_FILE|{filename}|{content.decode()}"
    return send_request(request)
