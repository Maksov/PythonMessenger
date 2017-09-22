# coding: utf-8
from socket import *
from sys import argv
import time
import jim

address = argv[1] if len(argv) > 1 else 'localhost'
port = int(argv[2]) if len(argv) > 2 else 7777

s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
s.bind((address, port))
s.listen(5)
print('Сервер запущен в {0}'.format(time.ctime(time.time())))

while True:
    client, addr = s.accept()  # Принять запрос на соединение
    print("Получен запрос на соединение от %s" % str(addr))
    data = client.recv(1024)
    if data:
        response = jim.parse_client_message(data.decode('ascii'))
        client.send(response.encode('ascii'))
        print(data.decode('ascii'))
        print(response)
    client.close()
