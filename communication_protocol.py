import socket
import json
import struct

import constants


class Client:
    __address: tuple[str, int]

    def __init__(self, ip_address: str = constants.GAME_HOSTING_IP_ADDRESS, port: int = constants.COMMUNICATION_PORT):
        self.__address = (ip_address, port)

    @staticmethod
    def __send_msg(msg: str, to: socket.socket):
        encoded_json_str = msg.encode()
        announcement = struct.pack("@I", len(encoded_json_str))  # size
        sent = to.send(announcement)

        # send size
        while sent < len(announcement):
            sent += to.send(announcement[sent:])

        #send content
        request = encoded_json_str
        sent = to.send(request)
        while sent < len(request):
            sent += to.send(request[sent:])
        print(f" {msg} : Message of {len(request)} bytes has been sent")

    def __config_socket(self) -> socket.socket:
        your_socket = socket.socket()
        try:
            your_socket.connect(self.__address)
        except OSError:
            raise OSError("connection failed in config_socket")
        return your_socket

    def sign_in_request(self, port: int = constants.RECEPTION_PORT, name: str = constants.NAME_TAG):
        tojson_dict = {
            "request": "subscribe",
            "port": port,
            "name": name,
            "matricules": [constants.MATRICULE]
        }
        current_socket = self.__config_socket()
        self.__send_msg(json.dumps(tojson_dict), current_socket)
        sign_in_result = Server.receive_msg_from_socket(current_socket)
        sign_in_result_dict = json.loads(sign_in_result)
        if sign_in_result_dict["response"] == "ok":
            print("signed in ok")
        elif sign_in_result_dict["response"] == "error":
            raise RuntimeError("failed sign in")
        else:
            raise RuntimeError("unexpected branching")
        current_socket.close()

    def pong_response(self, to: socket.socket):
        pong_request_dict = {
            "response": "pong"
        }
        json_str = json.dumps(pong_request_dict)
        self.__send_msg(json_str, to)
        to.close()

    def play_response(self, request_dict: dict, to: socket.socket):
        json_str = json.dumps(request_dict)
        self.__send_msg(json_str, to)
        to.close()

    @staticmethod
    def run(func):
        from time import sleep
        sleep(5)
        for i in range(10):
            try:
                func()
            except TypeError:
                TypeError("not callable")


class Server:
    __socket: socket.socket
    __address: tuple[str, int]

    def __init__(self, ip_address: str = constants.MY_IP, port: int = constants.RECEPTION_PORT):
        self.__address = (ip_address, port)
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

    def receive_msg(self) -> tuple[dict, socket.socket]:
        emitter = self.__accept_socket()
        buffer = emitter.recv(4)
        while len(buffer) != 4:
            buffer += emitter.recv(4-len(buffer))
        response_size = struct.unpack("@I", buffer)[0]  #getting size of msg
        received = emitter.recv(response_size)
        while len(received) < response_size:
            received += emitter.recv(response_size - len(received))

        #reading content
        json_dict = json.loads(received.decode())
        print(f" {json_dict} : Message of {response_size} bytes received")
        if json_dict.get("request") is not None:
            return json_dict, emitter
        else:
            raise RuntimeError("unexpected branching")

    @staticmethod
    def receive_msg_from_socket(to_listen_socket: socket.socket) -> str:
        buffer = to_listen_socket.recv(4)
        while len(buffer) != 4:
            buffer += to_listen_socket.recv(4 - len(buffer))
        response_size = struct.unpack("@I", buffer)[0]  # getting size of msg
        received = to_listen_socket.recv(response_size)
        while len(received) < response_size:
            received += to_listen_socket.recv(response_size - len(received))
        to_listen_socket.close()
        return received.decode()

    def run(self):
        while 1:
            print(self.receive_msg()[1])
