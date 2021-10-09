import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8821

MAX_MSG_SIZE = 1024


turn_on = True

while turn_on:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    client_msg, client_address = server_socket.recvfrom(MAX_MSG_SIZE)
    print("The client send:", client_msg.decode())
    server_socket.sendto("ok".encode(), client_address)
    if client_msg.decode() == "EXIT":
        turn_on = False
        end_msg = "תגובתך התקבלה במערכת ותטופל בהקדם.\n\t\t\t\tתודה שבחרתם בחברת נתי מדיה!"
        server_socket.sendto(end_msg.encode(), client_address)
        server_socket.close()



