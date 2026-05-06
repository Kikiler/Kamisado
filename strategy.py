import constants
import utils


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
                                                beta: float = float("+inf"), depth: int = 7) -> tuple[
        float, tuple[int, int] | None]:
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
