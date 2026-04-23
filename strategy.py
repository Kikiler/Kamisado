import random
from re import search

import constants
from copy import deepcopy
from collections import deque


class Strategy:

    @staticmethod
    def move(game_info: dict) -> dict:
        game_state = game_info["board"]
        color_to_play = game_info["color"]
        response_dict = dict()
        response_dict["response"] = "move"
        if game_info["players"][0] == constants.NAME_TAG:
            my_color = "dark"
            current_soldier_position = Strategy._retrieve_soldier(game_state, my_color, color_to_play)
            valid_moves = Strategy.valid_moves_for_black(game_state, current_soldier_position)
        else:
            my_color = "light"
            current_soldier_position = Strategy._retrieve_soldier(game_state, my_color, color_to_play)
            valid_moves = Strategy.valid_moves_for_white(game_state, current_soldier_position)
        if len(valid_moves) == 0:
            response_dict["response"] = "giveup"
            return response_dict
        response_dict["move"] = [current_soldier_position, random.choice(valid_moves)]
        response_dict["message"] = "alles < Nederlands "
        return response_dict

    @staticmethod
    def valid_moves_for_white(tensor: list[list], current_soldier_position: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier_position[0] + 1, 8):
            if tensor[i][current_soldier_position[1]] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1]))
        if current_soldier_position[1] + 1 < 7:
            for i in range(current_soldier_position[0] + 1, 8):
                if tensor[i][current_soldier_position[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier_position[1]))
        if 0 <= current_soldier_position[1] - 1:
            for i in range(current_soldier_position[0] + 1, 8):
                if tensor[i][current_soldier_position[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier_position[1]))
        return valid_moves_list

    def valid_moves_for_black(tensor: list[list], current_soldier_position: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier_position[0] - 1, -1, -1):
            if tensor[i][current_soldier_position[1]] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1]))
        if current_soldier_position[1] + 1 < 7:
            for i in range(current_soldier_position[0] - 1, -1, -1):
                if tensor[i][current_soldier_position[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier_position[1]))
        if 0 <= current_soldier_position[1] - 1:
            for i in range(current_soldier_position[0] - 1, -1, -1):
                if tensor[i][current_soldier_position[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier_position[1]))
        return valid_moves_list

    @staticmethod
    def _retrieve_soldier(tensor: list[list], my_color: str, to_play_color: str) -> tuple[int, int]:
        if to_play_color is not None:
            if my_color == "light":
                for i in range(8):
                    for j in range(8):
                        if tensor[i][j][1][0] == to_play_color and tensor[i][j][1][1] == my_color:
                            return i, j
                raise RuntimeError("unexpected branching")
            elif my_color == "dark":
                for i in range(7, -1, -1):
                    for j in range(7, -1, -1):
                        if tensor[i][j][1][0] == to_play_color and tensor[i][j][1][1] == my_color:
                            return i, j
                raise RuntimeError("unexpected branching")
            else:
                raise RuntimeError("unexpected branching")

        else:
            if my_color == "light":
                return 0, random.randint(0, 7)
            elif my_color == "dark":
                return 7, random.randint(0, 7)
            else:
                raise RuntimeError("unexpected branching")

    @staticmethod
    def _heuristic(tensor: list[list], my_color: str, valid_moves: list[tuple[int, int]]) -> tuple[int, int]:
        pass

    @staticmethod
    def _search(tensor: list[list], my_color: str, current_soldier_position: tuple[int, int], color_to_play: str) -> \
            tuple[int, int] | None:
        if my_color == "light":
            valid_moves = Strategy.valid_moves_for_white(tensor, current_soldier_position)
        else:
            valid_moves = Strategy.valid_moves_for_black(tensor, current_soldier_position)
        winning = Strategy._can_win(valid_moves, my_color)
        if winning is None:
            for move in valid_moves:
                new_tensor, new_color_to_play = Strategy._move_state(tensor, move, current_soldier_position, my_color,
                                                                     color_to_play)
                return Strategy._search(new_tensor, my_color, move, new_color_to_play)
        return winning

    def _can_win(positions: list[tuple[int, int]], my_color: str) -> tuple[int, int] | None:
        if my_color == "light":
            for position in positions:
                if position[0] == 7:
                    return position
        else:
            for position in positions:
                if position[0] == 0:
                    return position

    @staticmethod
    def _move_state(tensor: list[list], final: tuple[int, int], origin: tuple[int, int], my_color: str,
                    color_to_play: str) -> tuple[list[list], str]:
        return_tensor = deepcopy(tensor)
        return_tensor[final[0]][final[1]][1] = [color_to_play, my_color]
        return_tensor[origin[0]][origin[1]][1] = None
        return return_tensor, return_tensor[final[0]][final[1]][0]
