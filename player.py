from communication_protocol import Server, Client
import strategy


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
            if response[0]["request"] == "ping":
                self.__client.pong_response(response[1])
            elif response[0]["request"] == "play":
                print("should play now")
                self.__client.play_response(strategy.Strategy.move(response[0]["state"]), response[1])
            else:
                raise RuntimeError("unexpected branching")
