import random
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
        for i in range(100):
            if i % 2:
                soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                                       "dark",
                                                                       constants_test.STARTING_INFO["board"]
                                                                       [7][i % 8][1][0])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == "dark" and
                    constants_test.STARTING_INFO["board"]
                    [7][i % 8][1][0] == constants_test.STARTING_INFO["board"]
                    [soldier_position[0]][soldier_position[1]][1][0]
                    ,
                    "not our soldier")
            else:
                soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                                       "light",
                                                                       constants_test.STARTING_INFO["board"]
                                                                       [0][i % 8][1][0])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == "light" and
                    constants_test.STARTING_INFO["board"]
                    [0][i % 8][1][0] == constants_test.STARTING_INFO["board"]
                    [soldier_position[0]][soldier_position[1]][1][0]
                    ,
                    "not our soldier")
        tensor = constants_test.STARTING_INFO["board"]
        initial_pos = (0, 0)
        for i in range(100):
            valid_move = strategy.Strategy.valid_moves_for_white(tensor, initial_pos)
            move = random.choice(valid_move)
            color_to_play = tensor[move[0]][move[1]]
            tensor = strategy.Strategy._move_state(tensor, move, initial_pos, "white")
            #finish THIS FUNCTION

    def test_valid_moves(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves valid")
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")

        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "light",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves valid")
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")

        current_soldier_position = (0, 0)
        valid_moves = strategy.Strategy.valid_moves_for_white(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves permitted")
        all_valid_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                           (6, 6)]
        self.assertEqual(sorted(valid_moves), sorted(all_valid_moves), "method misses some valid moves")

        current_soldier_position = (7, 0)
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves permitted")
        all_valid_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5),
                           (1, 6)]
        self.assertEqual(sorted(valid_moves), sorted(all_valid_moves), "method misses some valid moves")

        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              (1, 0))
        self.assertTrue(len(valid_moves) == 0, "method misses some valid moves")

    def test_search(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        self.assertTrue(strategy.Strategy._search(constants_test.STARTING_INFO["board"],
                                                  "dark", current_soldier_position) != ())
        print(strategy.Strategy._search(constants_test.STARTING_INFO["board"],
                                        "dark", current_soldier_position))

    def test_move_state(self):
        current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"], "dark",
                                                                       constants_test.STARTING_INFO["color"])
        valid_moves = strategy.Strategy.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                              current_soldier_position)
        initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
        for move in valid_moves:
            new_tensor, new_color_to_play = strategy.Strategy._move_state(constants_test.STARTING_INFO["board"], move,
                                                                          current_soldier_position, "dark")
            self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
            self.assertTrue(new_tensor[move[0]][move[1]][1] == [constants_test.STARTING_INFO["board"]
                                                                [current_soldier_position[0]]
                                                                [current_soldier_position[1]][1][0], "dark"],
                            "return_tensor not changed at the correct place")
            self.assertTrue(new_color_to_play == initial_tensor[move[0]][move[1]][0], "wrong color to play")

            current_soldier_position = strategy.Strategy._retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                                           "light",
                                                                           constants_test.STARTING_INFO["color"])
            valid_moves = strategy.Strategy.valid_moves_for_white(constants_test.STARTING_INFO["board"],
                                                                  current_soldier_position)
            initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
        for move in valid_moves:
            new_tensor, new_color_to_play = strategy.Strategy._move_state(constants_test.STARTING_INFO["board"],
                                                                          move,
                                                                          current_soldier_position, "light")
            self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
            self.assertTrue(new_tensor[move[0]][move[1]][1] == [constants_test.STARTING_INFO["board"]
                                                                [current_soldier_position[0]][
                                                                    current_soldier_position[1]][1][0], "light"],
                            "return_tensor not changed at the correct place")
            self.assertTrue(new_color_to_play == initial_tensor[move[0]][move[1]][0], "wrong color to play")


if __name__ == '__main__':
    unittest.main()
