import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8821

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("Type here:")
    my_socket.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))
    print("client send:", msg)

    response, address = my_socket.recvfrom(1024)
    print("server send:", response.decode())

    if msg == "EXIT":
        response, address = my_socket.recvfrom(1024)
        print("server send:", response.decode())
        my_socket.close()
        break
