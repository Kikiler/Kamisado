import random
import constants


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

        response_dict["move"] = [current_soldier_position, random.choice(valid_moves)]
        response_dict["message"] = "alles < Nederlands "
        return response_dict

    @staticmethod
    def valid_moves_for_white(tensor: list[list], current_soldier: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier[0]+1,8):
            if tensor[i][current_soldier[1]] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier[1]))
        if current_soldier[1] + 1 < 7:
            for i in range(current_soldier[0]+1,8):
                if tensor[i][current_soldier[1]] is not None:
                    break
                else:
                        valid_moves_list.append((i, current_soldier[1]))
        if 0 <= current_soldier[1] - 1:
            for i in range(current_soldier[0]+1, 8):
                if tensor[i][current_soldier[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier[1]))
        return valid_moves_list

    def valid_moves_for_black(tensor: list[list], current_soldier: tuple[int, int]) -> list[tuple[int, int]]:
        valid_moves_list = list()
        for i in range(current_soldier[0] - 1, -1, -1):
            if tensor[i][current_soldier[1]] is not None:
                break
            else:
                valid_moves_list.append((i, current_soldier[1]))
        if current_soldier[1] + 1 < 7:
            for i in range(current_soldier[0] - 1, -1, -1):
                if tensor[i][current_soldier[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier[1]))
        if 0 <= current_soldier[1] - 1:
            for i in range(current_soldier[0] - 1, -1, -1):
                if tensor[i][current_soldier[1]] is not None:
                    break
                else:
                    valid_moves_list.append((i, current_soldier[1]))
        return valid_moves_list


    @staticmethod
    def _retrieve_soldier(tensor: list[list], my_color: str, to_play_color: str) -> tuple[int, int]:
        if to_play_color is not None:
            if my_color == "light":
                for i in range(8):
                    for j in range(8):
                        if tensor[i][j][1][0] == to_play_color and tensor[i][j][1][1] == my_color:
                            return i,j
                raise RuntimeError("unexpected branching")
            elif my_color == "dark":
                for i in range(7,-1,-1):
                    for j in range(7,-1,-1):
                        if tensor[i][j][1][0] == to_play_color and tensor[i][j][1][1] == my_color:
                            return i,j
                raise RuntimeError("unexpected branching")
            else:
                raise RuntimeError("unexpected branching")

        else:
            if my_color == "light":
                return 0, random.randint(0,7)
            elif my_color == "dark":
                return 7, random.randint(0, 7)
            else:
                raise RuntimeError("unexpected branching")



