CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"


PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "my_score_request": "MY_SCORE",
    "highscore_request_msg": "HIGHSCORE",
    "question_request": "GET_QUESTION",
    "answer_msg": "SEND_ANSWER",
    "users_logged": "LOGGED"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "your_score_msg": "YOUR_SCORE",
    "highscore_msg": "ALL_SCORE",
    "question_msg": "YOUR_QUESTION",
    "correct_answer": "CORRECT_ANSWER",
    "wrong_answer": "WRONG_ANSWER",
    "user_logged_msg": "LOGGED_ANSWER",
    "error_msg": "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    parsed_msg = data.split("|")
    if len(parsed_msg[0]) != 16 or len(parsed_msg) != 3 or len(parsed_msg[1]) != 4:
        cmd, msg = None, None
    else:
        parsed_msg[1] = parsed_msg[1].replace(" ", "")
        parsed_msg[0] = parsed_msg[0].replace(" ", "")

        if not parsed_msg[1].isnumeric() or int(parsed_msg[1]) != len(parsed_msg[2]):
            cmd, msg = None, None

        else:
            cmd = parsed_msg[0]
            msg = parsed_msg[2]
    return cmd, msg


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if type(data) == int:
        data = str(data)
    if type(cmd) != str or len(cmd) > 16 or len(data) > MAX_DATA_LENGTH:
        return None
    else:
        if type(data) != str:  # In case the data is  a collection and there is more than 1 field
            data = join_data(data)
        data_length = str(len(data)).rjust(4,"0")
        cmd = cmd.ljust(16)
        full_msg =f"{cmd}|{data_length}|{data}"

    return full_msg


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    number_of_fields = msg.count("#") + 1
    if number_of_fields != expected_fields:
        return [None]
    else:
        return msg.split("#")


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    joined_data = ""

    for i in range(len(msg_fields)):
        if i == len(msg_fields) - 1:
            joined_data += str(msg_fields[i])
        else:
            joined_data += str(msg_fields[i]) + "#"

    return joined_data




