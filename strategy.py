import numpy as np
import json
import random
import Constants


class Strategy:

    @staticmethod
    def move(game_info: dict) -> dict:
        game_state = game_info["board"]
        color_to_play = game_info["color"]
        response_dict = dict()
        my_color = "light"
        if game_info["players"][0] == Constants.NAME_TAG:
            my_color = "dark"
        response_dict["response"] = "move"
        valid_moves = Strategy.valid_moves(game_state, my_color,color_to_play)[1]
        response_dict["move"] = [valid_moves[0], random.choice(valid_moves[1])]
        response_dict["message"] = "alles < Nederlands "
        return response_dict

    @staticmethod
    def valid_moves(tensor: list[list], my_color: str, to_play_color: str) -> tuple[tuple[int,int], list]:
        valid_moves_list = list()
        current_soldier = Strategy.__retrieve_soldier(tensor, my_color, to_play_color)
        if my_color == "light":
            for i in range(current_soldier[0]+1,8):
                if tensor[i][current_soldier[1]][1][0] == "dark":
                    break
                else:
                    valid_moves_list.append((i, current_soldier[1]))
            if current_soldier[1] + 1 < 7:
                for i in range(current_soldier[0]+1,8):
                    if tensor[i][current_soldier[1]+1][1][0] == "dark":
                        break
                    else:
                            valid_moves_list.append((i, current_soldier[1]))
            if 0 <= current_soldier[1] - 1:
                for i in range(current_soldier[0]+1,8):
                    if tensor[i][current_soldier[1]-1][1][0] == "dark":
                        break
                    else:
                        valid_moves_list.append((i, current_soldier[1]))
        else:
            for i in range(current_soldier[0],-1,-1):
                if tensor[i][current_soldier[1]][1][0] == "light":
                    break
                else:
                    valid_moves_list.append((i, current_soldier[1]))
            if current_soldier[1] + 1 < 7:
                for i in range(current_soldier[0]+1,8):
                    if tensor[i][current_soldier[1]+1][1][0] == "light":
                        break
                    else:
                        valid_moves_list.append((i, current_soldier[1]))
            if 0 <= current_soldier[1] - 1:
                for i in range(current_soldier[0]+1,8):
                    if tensor[i][current_soldier[1]-1][1][0] == "light":
                        break
                    else:
                        valid_moves_list.append((i, current_soldier[1]))
        return current_soldier, valid_moves_list

    @staticmethod
    def __retrieve_soldier(tensor: list[list], my_color: str, to_play_color: str) -> tuple[int, int]:
        if to_play_color != "null":
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



