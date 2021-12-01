import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.219.100"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getAddr(self):
        return self.port

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except:
            return str(socket.error)
