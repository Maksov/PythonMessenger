import json
import time


def parse_client_message(msg):
    try:
        parsed_msg = json.loads(msg)
    except ValueError:
        return get_server_response(400, None, 'Incorrectly formed JSON'), None
    if 'action' in parsed_msg:
        action = parsed_msg['action']
        if action == 'presence':
            return get_server_response(200, 'OK', None), None
        if action == 'msg':
            if 'to' in parsed_msg:
                to = parsed_msg['to']
                if to.startswith('#'):
                    return get_server_response(200, 'OK', None), msg
                else:
                    pass
            else:
                return get_server_response(400, None, 'Incorrectly formed JSON'), None
    else:
        return get_server_response(400, None, 'Incorrectly formed JSON'), None


def get_server_response(response, alert, error):
    msg = ''
    timestr = time.ctime(time.time())
    if alert:
        msg = json.dumps({'response': response, 'time': timestr, 'alert': alert})
    if error:
        msg = json.dumps({'response': response, 'time': timestr, 'error': error})
    return msg
