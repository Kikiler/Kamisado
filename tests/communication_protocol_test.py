import unittest
import Constants
from communication_protocol import Server, Client
import threading


class ServerTest(unittest.TestCase):

    def test_pong_communication(self):
        client = Client(Constants.MY_IP, Constants.RECEPTION_PORT)
        thread = threading.Thread(target=client.run, args=[client.pong_request], daemon=True)
        thread.start()
        server = Server()
        self.assertEqual(server.receive_msg()[0], "response")
        self.assertEqual(server.receive_msg()[1]["response"], "pong")
        thread.join(5)

    def test_sign_in_communication(self):
        client = Client(Constants.MY_IP, Constants.RECEPTION_PORT)
        thread = threading.Thread(target=client.run, args=[client.sign_in_request], daemon=True)
        thread.start()
        server = Server()
        self.assertEqual(server.receive_msg()[0], "request")
        self.assertEqual(server.receive_msg()[1]["request"], "subscribe")
        thread.join(5)


if __name__ == '__main__':
    unittest.main()
