# coding: utf-8
from socket import *
from sys import argv
import time
import jimserver
import select
from log_config import log, configlogging

logger = configlogging(isserver=True)


@log(logger)
def checkcmdargs():
    args = ['localhost', 7777]
    args[0] = argv[1] if len(argv) > 1 else 'localhost'
    args[1] = int(argv[2]) if len(argv) > 2 else 7777
    return args


@log(logger)
def new_listen_socket(addr, port):
    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind((addr, port))
    sock.listen(5)
    sock.settimeout(0.2)
    return sock


@log(logger)
def mainloop():
    address, port = checkcmdargs()
    clients = []
    sock = new_listen_socket(address, port)
    print('Сервер запущен в {0}'.format(time.ctime(time.time())))

    while True:
        try:
            client, addr = sock.accept()  # Принять запрос на соединение
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(client)
        except OSError as e:
            pass
        else:
            data = client.recv(1024)
            if data:
                response, action = jimserver.parse_client_message(data.decode('ascii'))
                client.send(response.encode('ascii'))
                print(data.decode('ascii'))
                print(response)
                print(action)
        finally:
            w = []
            try:
                r, w, e = select.select(clients, clients, [], 0)
            except Exception as e:
                pass
            for s_client in r:
                try:
                    data = s_client.recv(1024)
                    if data:
                        response, action = jimserver.parse_client_message(data.decode('ascii'))
                        s_client.send(response.encode('ascii'))
                        print(data.decode('ascii'))
                        print(response)
                except ConnectionResetError:
                    clients.remove(s_client)
            for s_client in w:
                try:
                    if action:
                        s_client.send(action.encode(' ascii'))
                        print(action)
                except ConnectionResetError:
                    clients.remove(s_client)
            action = None  # action - костыль, просто сообщение, пока нет контроллера протокола


mainloop()
