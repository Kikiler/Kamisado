from communication_protocol import Server, Client


class Player:

    def __init__(self):
        self.__server = Server()
        self.__client = Client()

    """ 
    function coordinating the different classes to allow :
        - communication with the game handler (sending/receiving)
        - strategies to play the games
    """
    def play(self):
        self.__client.sign_in_request()
        while 1:
            response = self.__server.receive_msg()
            if response[0] == "request":
                if response[1] == "ping":
                    self.__client.pong_request()
                elif response[1] == "play":
                    print("should play now")
                else:
                    raise RuntimeError("unexpected branching")
            elif response[0] == "response":
                if response[1] == "error":
                    raise RuntimeError("failed sign in")
                elif response[1] == "ok":
                    print("correctly signed in")
                else:
                    raise RuntimeError("unexpected branching")
            else:
                raise RuntimeError("unexpected branching")


