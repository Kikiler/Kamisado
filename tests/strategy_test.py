import random
import unittest
from copy import deepcopy
import utils
import constants
import strategy
from tests import constants_test


class StrategyTest(unittest.TestCase):
    def test_retrieves_soldier(self):
        for i in range(100):
            if i % 2:
                soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == constants.SoldierColor.DARK,
                    "not our soldier")
            else:
                soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.LIGHT,
                                                          constants_test.STARTING_INFO["color"])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == constants.SoldierColor.LIGHT,
                    "not our soldier")
            self.assertTrue(0 <= soldier_position[0] < 8 and 0 <= soldier_position[1] < 8, "Indices are not in range")
        for i in range(100):
            if i % 2:
                soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["board"]
                                                          [7][i % 8][1][0])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == constants.SoldierColor.DARK and
                    constants_test.STARTING_INFO["board"]
                    [7][i % 8][1][0] == constants_test.STARTING_INFO["board"]
                    [soldier_position[0]][soldier_position[1]][1][0],
                    "not our soldier")
            else:
                soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.LIGHT,
                                                          constants_test.STARTING_INFO["board"]
                                                          [0][i % 8][1][0])
                self.assertTrue(
                    constants_test.STARTING_INFO["board"][soldier_position[0]][soldier_position[1]][1][
                        1] == constants.SoldierColor.LIGHT and
                    constants_test.STARTING_INFO["board"]
                    [0][i % 8][1][0] == constants_test.STARTING_INFO["board"]
                    [soldier_position[0]][soldier_position[1]][1][0],
                    "not our soldier")
        tensor = constants_test.STARTING_INFO["board"]
        initial_pos = (0, 0)
        counter = 0
        for i in range(100):
            valid_moves = utils.valid_moves_for_white(tensor, initial_pos)
            if len(valid_moves) == 0:
                print(f"no valid moves for {initial_pos} anymore after {i}th iterations ")
                if counter < 7:
                    counter += 1
                    initial_pos = (0, counter)
                    valid_moves = utils.valid_moves_for_white(tensor, initial_pos)
                    if len(valid_moves) == 0:
                        break
                else:
                    break

            move = random.choice(valid_moves)
            color_played = tensor[initial_pos[0]][initial_pos[1]][1][0]
            tensor, color = utils.move_state(tensor, move, initial_pos)
            initial_pos = utils.retrieve_soldier(tensor, constants.SoldierColor.LIGHT, color_played)
            self.assertTrue(initial_pos == move, "soldier not found")

    def test_valid_moves(self):
        current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        valid_moves = utils.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                  current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves valid")
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")

        current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.LIGHT,
                                                          constants_test.STARTING_INFO["color"])
        valid_moves = utils.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                  current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves valid")
        for moves in valid_moves:
            self.assertTrue(constants_test.STARTING_INFO["board"][moves[0]][moves[1]][1] is None,
                            "put an occupied place in valid moves")

        current_soldier_position = (0, 0)
        valid_moves = utils.valid_moves_for_white(constants_test.STARTING_INFO["board"],
                                                  current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves permitted")
        all_valid_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                           (6, 6)]
        self.assertEqual(sorted(valid_moves), sorted(all_valid_moves), "method misses some valid moves")

        current_soldier_position = (7, 0)
        valid_moves = utils.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                  current_soldier_position)
        self.assertTrue(len(valid_moves) <= 13, "maximum 13 moves permitted")
        all_valid_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5),
                           (1, 6)]
        self.assertEqual(sorted(valid_moves), sorted(all_valid_moves), "method misses some valid moves")

        valid_moves = utils.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                  (1, 0))
        self.assertTrue(len(valid_moves) == 0, "method misses some valid moves")

    def test_search(self):
        current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        self.assertTrue(strategy.Strategy._search_recursive(constants_test.STARTING_INFO["board"],
                                                            constants.SoldierColor.DARK,
                                                            current_soldier_position) != ())
        print(strategy.Strategy._search_recursive(constants_test.STARTING_INFO["board"],
                                                  constants.SoldierColor.DARK, current_soldier_position))

    def test_move_state(self):
        current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        valid_moves = utils.valid_moves_for_black(constants_test.STARTING_INFO["board"],
                                                  current_soldier_position)
        initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
        for move in valid_moves:
            new_tensor, new_color_to_play = utils.move_state(constants_test.STARTING_INFO["board"], move,
                                                             current_soldier_position)
            self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
            self.assertTrue(new_tensor[move[0]][move[1]][1] == constants_test.STARTING_INFO["board"]
            [current_soldier_position[0]]
            [current_soldier_position[1]][1], "return_tensor not changed at the correct place")
            self.assertTrue(new_color_to_play == initial_tensor[move[0]][move[1]][0], "wrong color to play")
            counter_dark = 0
            counter_light = 0
            for covector in new_tensor:
                for element in covector:
                    if element[1] is not None:
                        if element[1][1] is constants.SoldierColor.DARK.value:
                            counter_dark += 1
                        else:
                            counter_light += 1
            self.assertTrue(counter_light == 8 and counter_dark == 8, "deleted a soldier")

            current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                              constants.SoldierColor.LIGHT,
                                                              constants_test.STARTING_INFO["color"])
            valid_moves = utils.valid_moves_for_white(constants_test.STARTING_INFO["board"],
                                                      current_soldier_position)
            initial_tensor = deepcopy(constants_test.STARTING_INFO["board"])
        for move in valid_moves:
            new_tensor, new_color_to_play = utils.move_state(constants_test.STARTING_INFO["board"],
                                                             move,
                                                             current_soldier_position)
            self.assertEqual(initial_tensor, constants_test.STARTING_INFO["board"], "modified initial tensor")
            self.assertTrue(new_tensor[move[0]][move[1]][1] == [constants_test.STARTING_INFO["board"]
                                                                [current_soldier_position[0]][
                                                                    current_soldier_position[1]][1][0],
                                                                constants.SoldierColor.LIGHT],
                            "return_tensor not changed at the correct place")
            self.assertTrue(new_color_to_play == initial_tensor[move[0]][move[1]][0], "wrong color to play")
            counter_dark = 0
            counter_light = 0
            for covector in new_tensor:
                for element in covector:
                    if element[1] is not None:
                        if element[1][1] is constants.SoldierColor.DARK.value:
                            counter_dark += 1
                        else:
                            counter_light += 1
            self.assertTrue(counter_light == 8 and counter_dark == 8, "deleted a soldier")

    def test_informed_search(self):
        current_soldier_position = utils.retrieve_soldier(constants_test.STARTING_INFO["board"],
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        a= strategy.Strategy._informed_search(constants_test.STARTING_INFO["board"],
                                                 constants.SoldierColor.DARK, current_soldier_position)
        self.assertTrue(
            a in utils.valid_moves_for_black(constants_test.STARTING_INFO["board"], current_soldier_position))


    def test_informed_search_recursive(self):
        tensor = constants_test.STARTING_INFO["board"]
        black_soldier_position = utils.retrieve_soldier(tensor,
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        black_move = strategy.Strategy._informed_search_recursive(tensor,
                                                           constants.SoldierColor.DARK, black_soldier_position)
        self.assertTrue(black_move[1] in utils.valid_moves_for_black(tensor, black_soldier_position))
        tensor, playing_soldier_color = utils.move_state(tensor, black_move[1], black_soldier_position)
        white_soldier_position = utils.retrieve_soldier(tensor,
                                                          constants.SoldierColor.LIGHT,
                                                          playing_soldier_color)
        print(f"starting from : {black_soldier_position} to {black_move}")
        black_soldier_position = black_move[1]
        while (not utils.is_won(black_soldier_position, constants.SoldierColor.DARK) and
               not utils.is_won(white_soldier_position, constants.SoldierColor.LIGHT)):
            white_move = strategy.Strategy._informed_search_recursive(tensor,
                                                           constants.SoldierColor.LIGHT, white_soldier_position)[1]
            if white_move is not None:
                self.assertTrue(white_move in utils.valid_moves_for_white(tensor, white_soldier_position))
                tensor, playing_soldier_color = utils.move_state(tensor, white_move, white_soldier_position)
                white_soldier_position = white_move

            black_move = strategy.Strategy._informed_search_recursive(tensor,
                                                                      constants.SoldierColor.DARK,
                                                                      black_soldier_position)[1]
            if black_move is not None:
                self.assertTrue(black_move in utils.valid_moves_for_black(tensor, black_soldier_position))
                tensor, playing_soldier_color = utils.move_state(tensor, black_move, black_soldier_position)
                black_soldier_position = black_move
            if black_move is None and white_move is None:
                print("no one won")
                break
            print(f"black soldier position : {black_soldier_position} ")
            print(f"white soldier position : {white_soldier_position} ")
            utils.tensor_print(tensor)

    def test_informed_search_recursive_pruning(self):
        tensor = constants_test.STARTING_INFO["board"]
        black_soldier_position = utils.retrieve_soldier(tensor,
                                                          constants.SoldierColor.DARK,
                                                          constants_test.STARTING_INFO["color"])
        black_move = strategy.Strategy._informed_search_recursive_with_pruning(tensor,
                                                           constants.SoldierColor.DARK, black_soldier_position)
        self.assertTrue(black_move[1] in utils.valid_moves_for_black(tensor, black_soldier_position))
        tensor, playing_soldier_color = utils.move_state(tensor, black_move[1], black_soldier_position)
        white_soldier_position = utils.retrieve_soldier(tensor,
                                                          constants.SoldierColor.LIGHT,
                                                          playing_soldier_color)
        print(f"starting from : {black_soldier_position} to {black_move}")
        black_soldier_position = black_move[1]
        while (not utils.is_won(black_soldier_position, constants.SoldierColor.DARK) and
               not utils.is_won(white_soldier_position, constants.SoldierColor.LIGHT)):
            white_move = strategy.Strategy._informed_search_recursive_with_pruning(tensor,
                                                           constants.SoldierColor.LIGHT, white_soldier_position)[1]
            if white_move is not None:
                self.assertTrue(white_move in utils.valid_moves_for_white(tensor, white_soldier_position))
                tensor, playing_soldier_color = utils.move_state(tensor, white_move, white_soldier_position)
                white_soldier_position = white_move

            black_move = strategy.Strategy._informed_search_recursive_with_pruning(tensor,
                                                                      constants.SoldierColor.DARK,
                                                                      black_soldier_position)[1]
            if black_move is not None:
                self.assertTrue(black_move in utils.valid_moves_for_black(tensor, black_soldier_position))
                tensor, playing_soldier_color = utils.move_state(tensor, black_move, black_soldier_position)
                black_soldier_position = black_move
            if black_move is None and white_move is None:
                print("no one won")
                break
            print(f"black soldier position : {black_soldier_position} ")
            print(f"white soldier position : {white_soldier_position} ")
            utils.tensor_print(tensor)





if __name__ == '__main__':
    unittest.main()
