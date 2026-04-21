import socket
import json
import struct
import threading

from Constants import *


class Client:
    __address: tuple[str, int]
    __socket: socket.socket

    def __init__(self, port: int, host: str):
        self.__address = (host, port)

    def __send_msg(self, msg: str, ):
        self.__config_socket()
        encoded_json_str = msg.encode()
        announcement = struct.pack("@I", len(encoded_json_str))  # size
        sent = self.__socket.send(announcement)

        # send size
        while sent < len(announcement):
            sent += self.__socket.send(announcement[sent:])

        #send content
        request = encoded_json_str
        sent = self.__socket.send(request)
        while sent < len(request):
            sent += self.__socket.send(request[sent:])
        self.__socket.close()

        print(f" {msg} : Message of {len(request)} bytes has been sent")

    def __config_socket(self):
        self.__socket = socket.socket()
        try:
            self.__socket.connect(self.__address)
        except OSError:
            raise OSError("connection failed in config_socket")

    def sign_in_request(self, port: int):
        tojson_dict = {
            "request": "subscribe",
            "port": port,
            "name": NAME_TAG,
            "matricules": [MATRICULE]
        }
        self.__send_msg(json.dumps(tojson_dict))

    def pong_request(self):
        pong_request_dict = {
            "response": "pong"
        }
        json_str = json.dumps(pong_request_dict)
        self.__send_msg(json_str)

class Server:
    __socket: socket.socket
    __address: tuple[str, int]

    def __init__(self, host: str, port):
        self.__address = (host, port)
        self.__socket = socket.socket()
        try:
            self.__socket.bind(self.__address)
        except OSError:
            raise OSError('connection failed in server')
        self.__socket.listen()

    def __accept_socket(self):
        self.__socket.settimeout(10)
        while 1:
            try:
                emitter, address = self.__socket.accept()
                break
            except socket.timeout:
                print("timed out")
        return emitter

    def receive_msg(self) -> tuple[str, dict]:
        emitter = self.__accept_socket()
        response_size = struct.unpack("@I", emitter.recv(4))[0]  #getting size of msg
        received = emitter.recv(response_size)
        while len(received) < response_size:
            received += emitter.recv(response_size - len(received))
        emitter.close()

        #reading content
        json_dict = json.loads(received.decode())
        print(json_dict)
        if json_dict.get("response") is not None:
            return "response", json_dict.get("response")
        elif json_dict.get("request") is not None:
            return "request", json_dict.get("request")
        else:
            raise RuntimeError("unexpected branching")

    def sign_in(self):
        self.receive_msg()

    def run(self):
        pass


c = Client(COMMUNICATION_PORT, GAME_HOSTING_IP_ADDRESS)
s = Server(MY_IP, RECEPTION_PORT)
t = threading.Thread(target=s.sign_in, daemon=True)
t.start()
c.sign_in_request(RECEPTION_PORT)
while 1:
    response = s.receive_msg()
    if response[0] == "request":
        if response[1] == "ping":
            c.pong_request()
        elif response[1] == "play":
            print("should play now")
        else:
            raise RuntimeError("unexpected branching")
    elif response[0] == "response":
        if response[1] == "error":
            s.sign_in()
        elif response[1] == "ok":
            print("correctly signed in")
