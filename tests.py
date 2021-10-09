import socket
import json
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8821

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("The server is up...")

sockets_list = []
print("Waiting for clients...")

client_socket, client_address = server_socket.accept()

json.loads()

"""
{
    "login": "nati",
    "passoword": "admin",
    "score": 51
}
"""

