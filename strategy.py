import random
import constants
from copy import deepcopy
from queue import PriorityQueue


class Strategy:

    @staticmethod
    def move(game_info: dict) -> dict:
        game_state = game_info["board"]
        color_to_play = game_info["color"]
        response_dict = dict()
        response_dict["response"] = "move"
        if game_info["players"][0] == constants.NAME_TAG:
            team_color = constants.SoldierColor.DARK
            current_soldier_position = Strategy._retrieve_soldier(game_state, team_color, color_to_play)
            valid_moves = Strategy.valid_moves_for_black(game_state, current_soldier_position)
        else:
            team_color = constants.SoldierColor.LIGHT
            current_soldier_position = Strategy._retrieve_soldier(game_state, team_color, color_to_play)
            valid_moves = Strategy.valid_moves_for_white(game_state, current_soldier_position)

        if len(valid_moves) == 0:
            response_dict["response"] = "giveup"
            return response_dict
        response_dict["move"] = [current_soldier_position,
                                 Strategy._search_recursive(game_state, team_color, current_soldier_position)]
        response_dict["message"] = "alles < Nederlands "
        return response_dict

    @staticmethod
    def valid_moves_for_white(tensor: list[list], current_soldier_position: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier_position[0] + 1, 8):
            if tensor[i][current_soldier_position[1]][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1]))
        for i in range(current_soldier_position[0] + 1, 8):
            if 8 <= current_soldier_position[1] + i - current_soldier_position[0]:
                break
            if tensor[i][current_soldier_position[1] + i - current_soldier_position[0]][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1] + i - current_soldier_position[0]))
        for i in range(current_soldier_position[0] + 1, 8):
            if current_soldier_position[1] - i + current_soldier_position[0] < 0:
                break
            if tensor[i][current_soldier_position[1] - i + current_soldier_position[0]][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1] - i + current_soldier_position[0]))
        random.shuffle(valid_moves_list)
        return valid_moves_list

    @staticmethod
    def valid_moves_for_black(tensor: list[list], current_soldier_position: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier_position[0] - 1, -1, -1):
            if tensor[i][current_soldier_position[1]][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1]))
        for i in range(current_soldier_position[0] - 1, -1, -1):
            if 8 <= current_soldier_position[1] + current_soldier_position[0] - i:
                break
            if tensor[i][current_soldier_position[1] + current_soldier_position[0] - i][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1] + current_soldier_position[0] - i))
        for i in range(current_soldier_position[0] - 1, -1, -1):
            if current_soldier_position[1] - current_soldier_position[0] - i < 0:
                break
            elif tensor[i][current_soldier_position[1] - current_soldier_position[0] - i][1] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier_position[1] - current_soldier_position[0] - i))
        random.shuffle(valid_moves_list)
        return valid_moves_list

    @staticmethod
    def _retrieve_soldier(tensor: list[list], team_color: constants.SoldierColor, soldier_color: str) -> tuple[
        int, int]:
        if soldier_color is not None:
            if team_color is constants.SoldierColor.LIGHT:
                for i in range(8):
                    for j in range(8):
                        if tensor[i][j][1] is not None and tensor[i][j][1][0] == soldier_color and tensor[i][j][1][
                            1] == team_color.value:
                            return i, j
                raise RuntimeError("unexpected branching")
            elif team_color is constants.SoldierColor.DARK:
                for i in range(7, -1, -1):
                    for j in range(7, -1, -1):
                        if tensor[i][j][1] is not None and tensor[i][j][1][0] == soldier_color and tensor[i][j][1][
                            1] == team_color.value:
                            return i, j
                raise RuntimeError("unexpected branching")
            else:
                raise RuntimeError("unexpected branching")

        else:
            if team_color is constants.SoldierColor.LIGHT:
                return 0, random.randint(0, 7)
            elif team_color is constants.SoldierColor.DARK:
                return 7, random.randint(0, 7)
            else:
                raise RuntimeError("unexpected branching")

    @staticmethod
    def _heuristic(tensor: list[list], team_color: constants.SoldierColor) -> int:


    @staticmethod
    def _search_recursive(tensor: list[list], team_color: constants.SoldierColor,
                          current_soldier_position: tuple[int, int]) -> \
            tuple[int, int]:

        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = Strategy.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = Strategy.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        winning = Strategy._can_win(valid_moves, team_color)
        if winning is None:
            for move in valid_moves:
                new_tensor, playing_soldier_color = Strategy._move_state(tensor, move, current_soldier_position)
                winning = Strategy._search_recursive(new_tensor, other_team_color,
                                                     Strategy._retrieve_soldier(new_tensor, other_team_color,
                                                                                playing_soldier_color))
                if winning is not None:
                    return move
        return winning

    @staticmethod
    def _informed_search(tensor: list[list], team_color: constants.SoldierColor,
                         current_soldier_position: tuple[int, int]) -> \
            list[tuple[int, int]]:

        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = Strategy.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = Strategy.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        winning = Strategy._can_win(valid_moves, team_color)
        if winning is None:
            priority_q = PriorityQueue(len(valid_moves))
            solutions = list()
            for move in valid_moves:
                new_tensor, playing_soldier_color = Strategy._move_state(tensor, move, current_soldier_position)
                priority_q.put((Strategy._heuristic(new_tensor, team_color), (new_tensor, playing_soldier_color)))
            while not priority_q.empty():
                new_tensor, playing_soldier_color = priority_q.get()[1]
                solutions.append([current_soldier_position] +
                                 Strategy._informed_search(new_tensor, other_team_color,
                                                           Strategy._retrieve_soldier(new_tensor, other_team_color,
                                                                                      playing_soldier_color)))
            return min(solutions, key=lambda x: len(x))

        return [current_soldier_position, winning]

    @staticmethod
    def _can_win(positions: list[tuple[int, int]], team_color: constants.SoldierColor) -> tuple[int, int] | None:
        if team_color == constants.SoldierColor.LIGHT:
            for position in positions:
                if position[0] == 7:
                    return position
        else:
            for position in positions:
                if position[0] == 0:
                    return position
        return None

    """
        origin must be a soldier position
    """

    @staticmethod
    def _move_state(tensor: list[list], final: tuple[int, int], origin: tuple[int, int]) -> tuple[list[list], str]:

        return_tensor = deepcopy(tensor)
        return_tensor[final[0]][final[1]][1] = tensor[origin[0]][origin[1]][1]
        return_tensor[origin[0]][origin[1]][1] = None
        return return_tensor, return_tensor[final[0]][final[1]][0]
