# coding: utf-8
from socket import *
from sys import argv
from jimclient import get_presence_msg, parse_server_message, get_user_to_chat_msg
from log_config import log, configlogging

logger = configlogging(False)


@log(logger)
def checkcmdargs():
    args = ['localhost', 7777, '-r']  # -r - чтение, -w - запись
    args[0] = argv[1] if len(argv) > 1 else 'localhost'
    args[1] = int(argv[2]) if len(argv) > 2 else 7777
    args[2] = argv[3] if len(argv) > 3 else '-r'
    return args


s = socket(AF_INET, SOCK_STREAM)
address, port, mode = checkcmdargs()
s.connect((address, port))
s.send(get_presence_msg().encode('ascii'))
tm = s.recv(1024)
print(parse_server_message(tm.decode('ascii')))
if mode == '-r':
    while True:
        tm = s.recv(1024)
        print(tm.decode('ascii'))  # пока никак не парсим, еще не утрясли кодирование протокола
if mode == '-w':
    while True:
        text = input("Введите сообщение: ")
        if text == 'quit':
            break
        s.send(get_user_to_chat_msg(chatname='#all', text=text).encode('ascii'))
s.close()

