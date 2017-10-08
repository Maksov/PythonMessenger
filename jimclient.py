import json
import time


def get_presence_msg(type_status='online', account_name='client', status='test_status'):
    timestr = time.ctime(time.time())
    msg = json.dumps({'action': 'presence', 'time': timestr, 'type': type_status,
                      'user': {'account_name': account_name, 'status': status}})
    return msg


def get_quit_msg():
    timestr = time.ctime(time.time())
    msg = json.dumps({'action': 'quit', 'time': timestr})
    return msg


def get_user_to_chat_msg(chatname, text, account_name='guest'):
    timestr = time.ctime(time.time())
    chatname = '#' + chatname
    msg = json.dumps({'action': 'msg', 'time': timestr,
                      'to': chatname, 'from': account_name, 'message': text})
    return msg


def parse_server_message(msg):
    timestr = time.ctime(time.time())
    try:
        parsed_msg = json.loads(msg)
    except ValueError:
        return '{0}: Ошибка сервера: неизвестный ответ сервера'.format(timestr)
    if 'response' in parsed_msg:
        return '{0}: Ответ сервера: {1}, {2}'.format(
            parsed_msg['time'], parsed_msg['response'], parsed_msg['alert'])