# coding: utf-8
from socket import *
from sys import argv
import jim

address = argv[1] if len(argv) > 1 else 'localhost'
port = int(argv[2]) if len(argv) > 2 else 7777

s = socket(AF_INET, SOCK_STREAM)
s.connect((address, port))
s.send(jim.get_presence_msg().encode('ascii'))
tm = s.recv(1024)
print(jim.parse_message(tm.decode('ascii')))
s.close()

