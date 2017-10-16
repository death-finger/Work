from socket import *
from time import ctime
import os

HOST = ''
PORT = 20000
ADDR = (HOST, PORT)

with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(ADDR)
    s.listen(5)
    print('Listening...')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            data = data.decode('utf-8')
            if data == 'date':
                conn.send(bytes(ctime(), 'utf-8'))
            elif data == 'os':
                name = os.uname()
                conn.send(bytes(name, 'utf-8'))
            elif data[:2] == 'ls':
                if len(data) == 2:
                    conn.send(bytes(os.listdir(os.curdir()), 'utf-8'))
                else:
                    conn.send(bytes(os.listdir(data[3:]), 'utf-8'))
            else:
                conn.send(bytes('Hello [%s]' % data, 'utf-8'))
