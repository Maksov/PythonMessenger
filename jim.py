import time
import json


def get_presence_msg(type_status='online', account_name='client', status='test_status'):
    timestr = time.ctime(time.time())
    msg = json.dumps({'action': 'presence', 'time': timestr, 'type': type_status,
                      'user': {'account_name': account_name, 'status': status}})
    return msg


def get_quit_msg():
    timestr = time.ctime(time.time())
    msg = json.dumps({'action': 'quit', 'time': timestr})
    return msg


def parse_client_message(msg):
    try:
        parsed_msg = json.loads(msg)
    except ValueError:
        return get_server_response(400, None, 'Incorrectly formed JSON')
    if 'action' in parsed_msg:
        if parsed_msg['action'] == 'presence':
            return get_server_response(200, 'OK', None)
    else:
        return get_server_response(400, None, 'Incorrectly formed JSON')


def parse_server_message(msg):
    timestr = time.ctime(time.time())
    try:
        parsed_msg = json.loads(msg)
    except ValueError:
        return '{0}: Ошибка сервера: неизвестный ответ сервера'.format(timestr)
    if 'response' in parsed_msg:
        return '{0}: Ответ сервера: {1}, {2}'.format(
            parsed_msg['time'], parsed_msg['response'], parsed_msg['alert'])


def get_server_response(response, alert, error):
    msg = ''
    timestr = time.ctime(time.time())
    if alert:
        msg = json.dumps({'response': response, 'time': timestr, 'alert': alert})
    if error:
        msg = json.dumps({'response': response, 'time': timestr, 'error': error})
    return msg
