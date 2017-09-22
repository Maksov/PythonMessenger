import time
import json


def get_presence_msg(type_status='online', account_name='client', status='test_status'):
    timestr = time.ctime(time.time())
    msg = json.dumps({'action': 'presence', 'time': timestr, 'type': type_status,
                      'user': {'account_name': account_name, 'status': status}})
    return msg


def parse_message(msg):
    parsed_msg = json.loads(msg)
    if 'action' in parsed_msg:
        if parsed_msg['action'] == 'presence':
            return get_response(200, 'OK')
    if 'response' in parsed_msg:
        if parsed_msg['response'] == 200:
            return 'Ответ сервера: {0}, {1}'.format(parsed_msg['response'], parsed_msg['alert'])


def get_response(response, alert):
    msg = json.dumps({'response': response, 'alert': alert})
    return msg
