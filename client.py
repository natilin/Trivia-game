import socket
import chatlib

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678


def error_and_exit(error_msg):
    exit()


def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    #print(full_msg)

    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
    conn.send(msg.encode())
    #print("send: ", msg)


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        msg = [username, password]
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], msg)
        ans = chatlib.parse_message(conn.recv(1024).decode())
        if ans[0] == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Your'e logged")
            return
        else:
            print(ans[1])


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Logout\nGoodbye!")


def get_score(conn):
    ans = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score_request"], "")
    if None in ans or ans[0] != chatlib.PROTOCOL_SERVER["your_score_msg"]:
        print(ans)
    else:
        return ans[1]


def get_highscore(conn):
    ans = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["highscore_request_msg"], "")
    if None in ans or ans[0] != chatlib.PROTOCOL_SERVER["highscore_msg"]:
        print(ans)
    else:
        return ans[1]


def get_logged(conn):
    user_logged =  build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["users_logged"], "")
    if None in user_logged or user_logged[0] != chatlib.PROTOCOL_SERVER["user_logged_msg"]:
        print(user_logged)
    print("Users logged:\n", user_logged[1])


def print_question(msg):

    question = msg[1]
    print(question)

    ans_num = 1
    for n in range(2, 6):
        print(f"{ans_num}.", msg[n])
        ans_num += 1


def am_i_right(id_quest, user_ans, conn):
    msg = [id_quest, user_ans]
    res = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["answer_msg"], msg)
    if None in res or res[0] != chatlib.PROTOCOL_SERVER["correct_answer"] and res[0] != chatlib.PROTOCOL_SERVER[
        "wrong_answer"]:
        print(res)
    else:
        if res[0] == chatlib.PROTOCOL_SERVER["correct_answer"]:
            print("You right!")
        else:
            print(f"wrong!\nThe correct answer is: #{res[1]}")


def play_question(conn):
    ans = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["question_request"], "")
    if None in ans or ans[0] != chatlib.PROTOCOL_SERVER["question_msg"]:
        print(ans)
    else:
        ans_split = chatlib.split_data(ans[1], 6)
        id_quest = ans_split[0]
        print_question(ans_split)
        user_ans = input("What is the correct answer?(1-4)")
        am_i_right(id_quest, user_ans, conn)


def menu(conn):
    while True:
        print("\nWhat do you want to do?")
        print("\tp\tPlay trivia")
        print("\ts\tGet my score")
        print("\th\tGet highscore")
        print("\tl\tGet logged users")
        print("\tq\tQuit")

        user_command = input()
        if user_command == "p":
            play_question(conn)
        elif user_command == "s":
            print(get_score(conn))
        elif user_command == "h":
            print(get_highscore(conn))
        elif user_command == "l":
            get_logged(conn)
        elif user_command == "q":
            logout(conn)
            conn.close()
            break
        else:
            print("Invalid command")


def main():
    my_sock = connect()
    login(my_sock)
    print("Welcome to Trivia game!")
    menu(my_sock)


if __name__ == '__main__':
    main()




