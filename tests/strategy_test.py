import unittest
from copy import deepcopy

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

    def test_search(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        self.assertTrue(strategy.Strategy._search(constants_test.STARTING_INFO["board"],
                                                  "dark", current_soldier_position,
                                                  constants_test.STARTING_INFO["board"]
                                                  [current_soldier_position[0]][current_soldier_position[1]][0]))

    def test_move_state(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
        for move in valid_moves:
            new_tensor, new_color_to_play = strategy.Strategy._move_state(constants_test.STARTING_INFO["board"], move,
                                                                          current_soldier_position, "dark",
                                                                          constants_test.STARTING_INFO["board"]
                                                                          [current_soldier_position[0]][
                                                                              current_soldier_position[1]][0]
                                                                          )
            self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
            self.assertTrue(new_tensor[move[0]][move[1]][1] == [constants_test.STARTING_INFO["board"]
                                                                [current_soldier_position[0]][
                                                                    current_soldier_position[1]][0], "dark"],
                            "return_tensor not changed at the correct place")
            self.assertTrue(new_color_to_play == "light", "wrong color to play")

            current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                                           "light",
                                                                           constants_test.STARTING_INFO["color"])
            valid_moves = strategy.Strategy.valid_moves_for_white(constants_test.STARTING_INFO["board"],
                                                                  current_soldier_position)
            initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
            for move in valid_moves:
                new_tensor, new_color_to_play = strategy.Strategy._move_state(constants_test.STARTING_INFO["board"],
                                                                              move,
                                                                              current_soldier_position, "light",
                                                                              constants_test.STARTING_INFO["board"]
                                                                              [current_soldier_position[0]][
                                                                                  current_soldier_position[1]][0]
                                                                              )
                self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
                self.assertTrue(new_tensor[move[0]][move[1]][1] == [constants_test.STARTING_INFO["board"]
                                                                    [current_soldier_position[0]][
                                                                        current_soldier_position[1]][0], "light"],
                                "return_tensor not changed at the correct place")
                self.assertTrue(new_color_to_play == "dark", "wrong color to play")

    @staticmethod
    def isEqual(tensor1, tensor2) -> bool:
        pass


if __name__ == '__main__':
    unittest.main()
