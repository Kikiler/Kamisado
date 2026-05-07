import concurrent.futures
import threading
import time
from collections import defaultdict
import constants
import utils
import asyncio


class Strategy:

    @staticmethod
    def move(game_info: dict) -> dict:
        game_state = game_info["board"]
        color_to_play = game_info["color"]
        response_dict = dict()
        response_dict["response"] = "move"
        if game_info["players"][0] == constants.NAME_TAG:
            team_color = constants.SoldierColor.DARK
            current_soldier_position = utils.retrieve_soldier(game_state, team_color, color_to_play)
            valid_moves = utils.valid_moves_for_black(game_state, current_soldier_position)
        else:
            team_color = constants.SoldierColor.LIGHT
            current_soldier_position = utils.retrieve_soldier(game_state, team_color, color_to_play)
            valid_moves = utils.valid_moves_for_white(game_state, current_soldier_position)

        if len(valid_moves) == 0:
            response_dict["move"] = [current_soldier_position, current_soldier_position]
            response_dict["message"] = "alles < Nederlands "
            return response_dict
        response_dict["move"] = [current_soldier_position,
                                 Strategy._informed_search(game_state, team_color, current_soldier_position)]
        response_dict["message"] = "alles < Nederlands "
        return response_dict

    @staticmethod
    def _heuristic(tensor: list[list], team_color: constants.SoldierColor, current_soldier_position: tuple[int, int],
                   next_playing_soldier_position: tuple[int, int]) -> float:
        if team_color is constants.SoldierColor.LIGHT.value:
            valid_moves = utils.valid_moves_for_black(tensor, next_playing_soldier_position)
            if utils.can_win(valid_moves, constants.SoldierColor.LIGHT) is not None:
                return float('+inf')
            return round(len(valid_moves) /
                         constants.static_dangerosity_tensor_white[current_soldier_position[0]][
                             current_soldier_position[1]], 2)
        else:
            valid_moves = utils.valid_moves_for_white(tensor, next_playing_soldier_position)
            if utils.can_win(valid_moves, constants.SoldierColor.DARK) is not None:
                return float('+inf')
            return round(len(valid_moves) /
                         constants.static_dangerosity_tensor_black[current_soldier_position[0]][
                             current_soldier_position[1]], 2)

    @staticmethod
    def _search_recursive(tensor: list[list], team_color: constants.SoldierColor,
                          current_soldier_position: tuple[int, int]) -> \
            tuple[int, int]:

        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = utils.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = utils.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        winning = utils.can_win(valid_moves, team_color)
        if winning is None:
            for move in valid_moves:
                new_tensor, playing_soldier_color = utils.move_state(tensor, move, current_soldier_position)
                winning = Strategy._search_recursive(new_tensor, other_team_color,
                                                     utils.retrieve_soldier(new_tensor, other_team_color,
                                                                            playing_soldier_color))
                if winning is not None:
                    return move
        return winning

    @staticmethod
    def _informed_search(tensor: list[list], team_color: constants.SoldierColor,
                         current_soldier_position: tuple[int, int]) -> \
            tuple[int, int]:

        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = utils.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = utils.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        winning = utils.can_win(valid_moves, team_color)
        if winning is None:
            current_state_value = float("+inf")
            for move in valid_moves:
                new_tensor, playing_soldier_color = utils.move_state(tensor, move, current_soldier_position)
                next_state_value = Strategy._heuristic(new_tensor, team_color, move,
                                                       utils.retrieve_soldier(new_tensor, other_team_color,
                                                                              playing_soldier_color))
                if next_state_value < current_state_value:
                    current_state_value = next_state_value
                    winning = move
        return winning

    @staticmethod
    def _informed_search_recursive(tensor: list[list], team_color: constants.SoldierColor,
                                   current_soldier_position: tuple[int, int], depth: int = 5) -> tuple[
        float, tuple[int, int] | None]:
        if utils.is_won(current_soldier_position, team_color) or depth == 0:
            return Strategy.heuristic_in_place(tensor, team_color, current_soldier_position), current_soldier_position
        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = utils.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = utils.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        current_value = float("+inf")
        winning = None
        for move in valid_moves:
            new_tensor, playing_soldier_color = utils.move_state(tensor, move, current_soldier_position)
            value, _ = Strategy._informed_search_recursive(new_tensor, other_team_color,
                                                           utils.retrieve_soldier(new_tensor,
                                                                                  other_team_color,
                                                                                  playing_soldier_color), depth - 1)
            if value < current_value:
                current_value = value
                winning = move
        return current_value, winning

    @staticmethod
    def heuristic_in_place(tensor: list[list], team_color: constants.SoldierColor,
                           current_soldier_position: tuple[int, int], ) \
            -> float:
        if team_color is constants.SoldierColor.LIGHT.value:
            valid_moves = utils.valid_moves_for_black(tensor,
                                                      utils.retrieve_soldier(tensor, constants.SoldierColor.DARK,
                                                                             tensor[current_soldier_position[0]][
                                                                                 current_soldier_position[1]][0]))
            if utils.can_win(valid_moves, constants.SoldierColor.LIGHT) is not None:
                return float('+inf')
            return round(len(valid_moves) /
                         constants.static_dangerosity_tensor_white[current_soldier_position[0]][
                             current_soldier_position[1]], 2)
        else:
            valid_moves = utils.valid_moves_for_white(tensor,
                                                      utils.retrieve_soldier(tensor, constants.SoldierColor.LIGHT,
                                                                             tensor[current_soldier_position[0]][
                                                                                 current_soldier_position[1]][0]))
            if utils.can_win(valid_moves, constants.SoldierColor.DARK) is not None:
                return float('+inf')
            return round(len(valid_moves) /
                         constants.static_dangerosity_tensor_black[current_soldier_position[0]][
                             current_soldier_position[1]], 2)

    @staticmethod
    def _informed_search_recursive_with_pruning(tensor: list[list], team_color: constants.SoldierColor,
                                                current_soldier_position: tuple[int, int], alpha: float = float("-inf"),
                                                beta: float = float("+inf"), depth: int = 7) \
            -> tuple[float, tuple[int, int] | None]:
        if utils.is_won(current_soldier_position, team_color) or depth == 0:
            return -Strategy.heuristic_in_place(tensor, team_color, current_soldier_position), current_soldier_position
        if team_color is constants.SoldierColor.LIGHT:
            valid_moves = utils.valid_moves_for_white(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.DARK
        else:
            valid_moves = utils.valid_moves_for_black(tensor, current_soldier_position)
            other_team_color = constants.SoldierColor.LIGHT
        current_value = float("+inf")
        winning = None
        for move in valid_moves:
            new_tensor, playing_soldier_color = utils.move_state(tensor, move, current_soldier_position)
            value, _ = Strategy._informed_search_recursive_with_pruning(new_tensor, other_team_color,
                                                                        utils.retrieve_soldier(new_tensor,
                                                                                               other_team_color,
                                                                                               playing_soldier_color),
                                                                        -beta, -alpha, depth - 1)
            if value <= current_value:
                current_value = value
                winning = move
            beta = min(beta, current_value)
            if beta <= alpha:
                #print(f"pruned with alpha: {alpha} and beta: {beta} at depth: {depth}")
                break
        return -current_value, winning

    @staticmethod
    async def _informed_search_recursive_with_pruning_iteratively_deepening(tensor: list[list],
                                                                            team_color: constants.SoldierColor,
                                                                            current_soldier_position: tuple[int, int],
                                                                            timeout: float) \
            -> tuple[int, int]:
        cache = defaultdict(lambda: float("+inf"))

        async def _informed_search_recursive_with_pruning_in_func(tensor: list[list],
                                                                  team_color: constants.SoldierColor,
                                                                  current_soldier_position: tuple[int, int], depth: int,
                                                                  alpha: float = float("-inf"),
                                                                  beta: float = float("+inf")) \
                -> tuple[float, tuple[int, int] | None]:
            if utils.is_won(current_soldier_position, team_color) or depth == 0:
                return -Strategy.heuristic_in_place(tensor, team_color,
                                                    current_soldier_position), current_soldier_position
            if team_color is constants.SoldierColor.LIGHT:
                valid_moves = utils.valid_moves_for_white(tensor, current_soldier_position)
                other_team_color = constants.SoldierColor.DARK
            else:
                valid_moves = utils.valid_moves_for_black(tensor, current_soldier_position)
                other_team_color = constants.SoldierColor.LIGHT
            current_value = float("+inf")
            winning = None
            possibilities = [(current_soldier_position, valid_move) for
                             valid_move in valid_moves]
            possibilities.sort(key=lambda poss: cache[poss])
            for move in valid_moves:
                new_tensor, playing_soldier_color = utils.move_state(tensor, move, current_soldier_position)
                await asyncio.sleep(0)
                value, _ = await _informed_search_recursive_with_pruning_in_func(new_tensor, other_team_color,
                                                                                 utils.retrieve_soldier(new_tensor,
                                                                                                        other_team_color,
                                                                                                        playing_soldier_color),
                                                                                 depth - 1,
                                                                                 - beta, -alpha)
                if value <= current_value:
                    current_value = value
                    winning = move
                beta = min(beta, current_value)
                if beta <= alpha:
                    # print(f"pruned with alpha: {alpha} and beta: {beta} at depth: {depth}")
                    break
            cache[(current_soldier_position, winning)] = -current_value
            return -current_value, winning

        current_value, current_move = float("+inf"), current_soldier_position
        value, move = current_value, current_move

        async def check_timeout(start: float) -> None:
            while 1:
                if timeout <= time.time() - start:
                    #print(time.time() - start)
                    raise RuntimeError("time over")
                await asyncio.sleep(0)

        depth = 1
        start = time.time()
        task = asyncio.create_task(check_timeout(start))
        while time.time() - start < timeout:
            try:
                current_value, current_move = await _informed_search_recursive_with_pruning_in_func(tensor, team_color,
                                                                                                    current_soldier_position,
                                                                                                    depth, timeout - (
                                                                                                            time.time() - start))
                value, move = current_value, current_move
                #print(f"from {current_soldier_position} to {move} with value : {value} at depth : {depth} "
                      #f"with {round(time.time() - start, 3)} seconds spent and "
                      #f"thus {round(timeout - time.time() + start, 3)} seconds left")
                depth += 1
                await task
            except RuntimeError:
                break
        #print('depth =', depth)
        #print(f"time spent running : {round(time.time() - start, 3)} ")
        #print(move)
        return move
