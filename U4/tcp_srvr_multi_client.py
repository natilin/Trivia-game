import socket
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8821

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("The server is up...")

sockets_list = []
print("Waiting for clients...")

while True:
    ready_to_read, ready_to_write, in_error = select.select([server_socket] + sockets_list, [], [])
    for current_socket in ready_to_read:
        if current_socket is server_socket:
            client_socket, client_address = current_socket.accept()
            print("New client connected:", client_address)
            sockets_list.append(client_socket)
        else:
            print("New data from client")
            data = current_socket.recv(1021).decode()
            if data == "":
                print("connection closed", current_socket.getpeername())
                sockets_list.remove(current_socket)
                current_socket.close()
            else:
                print(data)
                current_socket.send(data.encode())

