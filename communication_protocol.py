import socket
import json
import struct


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

    def sign_in(self, port: int) -> tuple[socket.socket, tuple[str, int]]:
        tojson_dict = {
            "request": "subscribe",
            "port": port,
            "name": "roofdier",
            "matricules": ["24330", "24330"]
        }
        json_str = json.dumps(tojson_dict)
        encoded_json_str = json_str.encode()
        announcement = struct.pack("@I", len(encoded_json_str))
        sent = self.__socket.send(announcement)

        while sent < len(announcement):
            sent += self.__socket.send(announcement[sent:])
        print("sent")

        request = encoded_json_str
        sent = self.__socket.send(request)
        while sent < len(request):
            sent += self.__socket.send(request[sent:])
        print("sent")
        return self.__socket, (self.__address[0], port)


class Server:
    __socket: socket.socket
    __address: tuple[str, int]

    def __init__(self, sign_in_socket: socket.socket, sign_in_address: tuple[str, int]):
        self.__socket = sign_in_socket
        self.__address = sign_in_address

    def sign_in(self):
        response = struct.unpack_from("@s",self.__socket.recv(1024), 3)[0].decode()
        print(response)
        json_dict = json.loads(response)
        if json_dict["response"] == "ok":
            print("succeeded")
        else:
            print("failed")
        self.__socket.close()


c = Client(3000, "172.17.10.41")
communication_socket, communication_address = c.sign_in(4000)
s = Server(communication_socket, communication_address)
s.sign_in()
