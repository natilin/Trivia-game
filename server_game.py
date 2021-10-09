import socket
import chatlib
import random

# GLOBALS
users = {
    "Nati": { "password": "123", "score": 0, "questions_asked": []},
    "Shira": {"password": "123", "score": 0, "questions_asked": []}
        }
questions = {
    2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
    4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
           "correct": 3}
            }
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
socket_lst = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"

msg_to_send = []


def setup_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", SERVER_PORT))
    server_socket.listen()
    print("server is up and running")

    return server_socket


def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
    msg_to_send.append((conn, msg))
    #conn.send(msg.encode())

    #print("[SERVER] ", conn.getpeername(), msg)  # Debug print


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ", conn.getpeername(), full_msg)  # Debug print

    return cmd, data


def handle_login_message(conn, data):
    login_data = chatlib.split_data(data, 2)
    if login_data == [None]:
        print(login_data)
    else:
        user_name = login_data[0]
        password = login_data[1]
        if user_name not in users or password != users[login_data[0]]["password"]:
            send_error(conn, "user name or password is incorrect!")
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
            logged_users[conn.getpeername()] = user_name


def handle_logout_message(conn):
    print("Disconnecting", conn.getpeername())
    socket_lst.remove(conn.getpeername())
    conn.close()


def handle_getscore_message(conn, username):
    user_score = users[username]["score"]
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], user_score)


def handle_highscore_message(conn):
    sorted_score = sorted(users, key=lambda value: value[3], reverse=True)
    high_score_msg = ""
    for name in sorted_score:
        high_score_msg += f"{name}:{users[name]['score']}" + "\n"
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["highscore_msg"], high_score_msg)

def load_questions():
    return questions


def create_random_question():
    quest_list = load_questions()
    random_num = random.choice(list(quest_list))
    return [random_num, quest_list[random_num]["question"]] + quest_list[random_num]["answers"]
    

def handle_question_message(conn):
    question = create_random_question()
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["question_msg"], question)


def handle_answer_message(conn,username, data):
    ques_num, user_ans= data.split("#")
    correct_ans = questions[int(ques_num)]["correct"]
    if correct_ans == int(user_ans):
        users[username]["score"] += 5
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer"], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer"], correct_ans)


def handle_client_message(conn):
    try:
        code, data = recv_message_and_parse(conn)
    except:
        handle_logout_message(conn)
        return

    if code == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif code == chatlib.PROTOCOL_CLIENT["logout_msg"] or code == "":
        handle_logout_message(conn)

    elif code == chatlib.PROTOCOL_CLIENT["my_score_request"]:
        handle_getscore_message(conn, logged_users[conn.getpeername()])
    elif code == chatlib.PROTOCOL_CLIENT["highscore_request_msg"]:
        handle_highscore_message(conn)
    elif code == chatlib.PROTOCOL_CLIENT["question_request"]:
        handle_question_message(conn)
    elif code == chatlib.PROTOCOL_CLIENT["answer_msg"]:
        handle_answer_message(conn,logged_users[conn.getpeername()], data)
    else:
        send_error(conn, "Invalid message received")


def main():
    server_socket = setup_socket()

    while True:
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)
        socket_lst.append(client_address)
        while socket_lst:
            handle_client_message(client_socket)


if __name__ == '__main__':
    main()




