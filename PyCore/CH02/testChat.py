from socket import *
from time import ctime

HOST = ''
PORT = 20000
ADDR = (HOST, PORT)
BUFF = 1024

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('Waiting for connect...')
    conn, addr = tcpSerSock.accept()
    print('Connected from %s at %s' % (addr, ctime()))
    while True:
        data = conn.recv(BUFF)
        if not data: break
        if data == 'Quit':
            conn.close()
        else:
            print("[%s]%s said %s" % (ctime(), addr, data.decode('utf-8')))
        senddata = ''
        while senddata == '':
            senddata = input('reply> ')
        conn.send(bytes("[%s] %s said %s" % (ctime(), 'SRVR', senddata), 'utf-8'))
        data = None

conn.close()