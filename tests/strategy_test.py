import unittest
import strategy
from tests import constants_test


class StrategyTest(unittest.TestCase):
    def test_retrieves_soldier(self):
        for i in range(100):
            if i % 2:
                soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][1] == "dark",
                    "not our soldier")
            else:
                soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "light",
                                                                       constants_test.STARTING_INFO["color"])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][1] == "light",
                    "not our soldier")
            self.assertTrue(0 <= soldier_position[0] < 8 and 0 <= soldier_position[1] < 8, "Indices are not in range")

    def test_valid_moves(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")

        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "light",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")




if __name__ == '__main__':
    unittest.main()
