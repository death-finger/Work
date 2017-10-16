from socketserver import TCPServer as TCP, StreamRequestHandler as SRH
from time import ctime

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)

class MyRequestHandler(SRH):
    def handler(self):
        print('...connected from:', self.client_address)
        self.data = ctime() + self.rfile.readline().strip()
        self.wfile.write(self.data)

tcpServ = TCP(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()