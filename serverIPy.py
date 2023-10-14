import socket

class Server():
    def __init__(self):
        self.__HOST = ""
        self.__PORT = 7777
        self.__ADDR = (self.__HOST, self.__PORT)
        self.__SIZE = 64       
        self.__DISCONNECT_COMMAND = ["!disconnect", "!d"]
        self.MSGglobal = None

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.__ADDR)
        
        self.users = []

    def __update(self):
        self.__ADDR = (self.__HOST, self.__PORT)
        self.__server.bind(self.__ADDR)

    def setHost(self, newHost):
        self.__HOST = newHost
        self.__update()

    def setPort(self, newPort):
        self.__PORT = newPort
        self.__update()

    def client_get(self):        
        msg = self.conn.recv(self.__SIZE).decode('utf-8')
        if msg:
            self.MSGglobal = msg
            if msg.lower() in self.__DISCONNECT_COMMAND:
                self.conn.send(b"disconnected")
                self.conn.close()

    def send2(self,text):
            msg = text.encode('utf-8')
            msg_len = len(text)
            send_len = str(msg_len).encode('utf-8')
            send_len += b" " * (self.__SIZE - len(send_len))
            self.conn.send(msg)


    def start(self):
        try:
            self.__server.bind(self.__ADDR)
        except:
            pass
        print("[STARTING]")
        self.__server.listen(1)
        print("[LISTENING]")

        self.conn, self.addrclient = self.__server.accept()
