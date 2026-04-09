import socket
import json


class Client:
    __address: tuple[str, int]
    __socket: socket.socket

    def __init__(self, port: int, host: str):
        self.__address = (host, port)
        self.__socket = socket.socket()
        try:
            self.__socket.connect(self.__address)
        except OSError:
            print("connection failed", OSError)

    def sign_in(self, port: int):
        tojson_dict = {
            "request": "subscribe",
            "port": port,
            "name": "roofdier",
            "matricules": ["24330", "24330"]
        }
        json_str = json.dumps(tojson_dict)
        encoded_json_str = json_str.encode()
        sent = self.__socket.send(encoded_json_str, 1024)
        while sent < len(json_str):
            sent += self.__socket.send(encoded_json_str[sent:])
        print("sent")
        self.__socket.close()


class Server:
    __address: tuple[str, int]
    __socket: socket.socket

    def __init__(self, port: int, host: str):
        self.__address = (host, port)
        self.__socket = socket.socket()
        try:
            self.__socket.bind(self.__address)
        except OSError:
            print("connection failed", OSError)
        self.__socket.listen()

    def sign_in(self):
        self.__socket.settimeout(5)
        while 1:
            try:
                server, address = self.__socket.accept()
                break
            except socket.timeout:
                pass
        json_str = server.recv(1024).decode()
        json_dict = json.loads(json_str)
        if json_dict["response"] == "ok":
            print("succeeded")
        else:
            print("failed")
        self.__socket.close()


c = Client(3000, "172.17.10.41")
c.sign_in(4000)
s = Server(4000, "172.17.10.41")
s.sign_in()
