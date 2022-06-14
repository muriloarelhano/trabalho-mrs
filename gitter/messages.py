from copy import copy


def clear_messages(messages):
    copy_messages = copy(messages)
    for idx, message in enumerate(copy_messages):
        for key in list(message):
            if type(message[key]) == dict or  type(message[key]) == list:
                del messages[idx][key]
    return messages
