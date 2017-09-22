from unittest import TestCase
import jim
import json
import time

class TestJIM(TestCase):
    def test_get_quit_msg(self):
        msg = jim.get_quit_msg()
        msg_parsed = json.loads(msg)
        assert msg_parsed['action'] == 'quit'
        assert 'time' in msg_parsed

    def test_get_presence_msg(self):
        msg = jim.get_presence_msg()
        msg_parsed = json.loads(msg)
        assert msg_parsed['action'] == 'presence'
        assert 'time' in msg_parsed
        assert 'type' in msg_parsed
        assert 'user' in msg_parsed

    def test_parse_client_message(self):
        timestr = time.ctime(time.time())
        msg = json.dumps({'action': 'presence', 'time': timestr, 'type': 'online',
                          'user': {'account_name': 'test', 'status': 'test_status'}})
        response = jim.parse_client_message(msg)
        response_parsed = json.loads(response)
        assert response_parsed['response'] == 200
        assert response_parsed['alert'] == 'OK'
        assert 'time' in response_parsed

        msg = json.dumps({'not_action!': 'presence', 'time': timestr, 'type': 'online',
                          'user': {'account_name': 'test', 'status': 'test_status'}})
        response = jim.parse_client_message(msg)
        response_parsed = json.loads(response)
        assert response_parsed['response'] == 400
        assert 'error' in response_parsed
        assert 'time' in response_parsed

    def test_parse_server_message(self):
        msg = json.dumps({'response': 200, 'time': 'testtime', 'alert': 'OK'})
        response = jim.parse_server_message(msg)
        assert 'Ответ сервера' in response

    def test_get_server_response(self):
        response = jim.get_server_response(200, 'OK', None)
        response_parsed = json.loads(response)
        assert response_parsed['response'] == 200
        assert response_parsed['alert'] == 'OK'
        assert 'time' in response_parsed