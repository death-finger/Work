from socket import *

HOST = 'localhost'
PORT = 20000
ADDR = (HOST, PORT)

conn = socket(AF_INET, SOCK_STREAM)
conn.connect(ADDR)

while True:
    data = input('> ')
    conn.send(bytes(data, 'utf-8'))
    data = conn.recv(1024)
    print('Received', data.decode('utf-8'))