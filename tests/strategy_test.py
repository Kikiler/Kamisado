import unittest
import strategy
from tests import constants_test


class StrategyTest(unittest.TestCase):
    def test_retrieves_soldier(self):
        for i in range(100):
            soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark", constants_test.STARTING_INFO["color"])
            self.assertTrue(0 <= soldier_position[0] < 8 and 0 <= soldier_position[1] < 8)
        print("Index are in range")

    def test_valid_moves(self):
        pass





if __name__ == '__main__':
    unittest.main()
