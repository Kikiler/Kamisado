import unittest
from communication_protocol import Server, Client
import constants
import threading


class ServerTest(unittest.TestCase):
    def test_sign_in_communication(self):
        client = Client(constants.MY_IP, constants.RECEPTION_PORT)
        thread = threading.Thread(target=client.run, args=[client.sign_in_request], daemon=True)
        thread.start()
        server = Server()
        self.assertEqual(server.receive_msg()[0]["request"], "subscribe")
        thread.join(5)


if __name__ == '__main__':
    unittest.main()
