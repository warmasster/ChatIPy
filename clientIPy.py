import socket

class Client():
    def __init__(self):
        self.__IP = ""
        self.__PORT = 7777
        self.__ADDR = (self.__IP, self.__PORT)
        self.__SIZE = 64
        self.connected = False
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.MSGglobal = None

    def connect(self):
        try:
            self.connected = True
            self.__ADDR = (self.__HOST, self.__PORT)
            self.__client.connect(self.__ADDR)
        except:
            pass

    def setHost(self, newHost):
        self.__HOST = newHost

    def setPort(self, newPort):
        self.__PORT = int(newPort) if type(newPort) != int else newPort

    def recive(self):
        servermsg = self.__client.recv(self.__SIZE).decode("utf-8")
        if not servermsg.isnumeric():
            self.MSGglobal = servermsg
        if servermsg == "disconnected":
            self.__client.close()
            self.connected = False

    def send(self,text):
        msg = text.encode('utf-8')
        msg_len = len(text)
        send_len = str(msg_len).encode('utf-8')
        send_len += b" " * (self.__SIZE - len(send_len))
        self.__client.send(msg)

