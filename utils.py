import constants
import random
from copy import deepcopy


def can_win(positions: list[tuple[int, int]], team_color: constants.SoldierColor) -> tuple[int, int] | None:
    if team_color == constants.SoldierColor.LIGHT:
        for position in positions:
            if position[0] == 7:
                return position
    else:
        for position in positions:
            if position[0] == 0:
                return position
    return None


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


def retrieve_soldier(tensor: list[list], team_color: constants.SoldierColor, soldier_color: str) \
        -> tuple[int, int]:
    if soldier_color is not None:
        if team_color is constants.SoldierColor.LIGHT:
            for i in range(8):
                for j in range(8):
                    if (tensor[i][j][1] is not None and tensor[i][j][1][0] == soldier_color and
                            tensor[i][j][1][1] == team_color.value):
                        return i, j
            raise RuntimeError("unexpected branching")
        elif team_color is constants.SoldierColor.DARK:
            for i in range(7, -1, -1):
                for j in range(7, -1, -1):
                    if (tensor[i][j][1] is not None and tensor[i][j][1][0] == soldier_color and
                            tensor[i][j][1][1] == team_color.value):
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


"""
        origin must be a soldier position
    """


def move_state(tensor: list[list], final: tuple[int, int], origin: tuple[int, int]) -> tuple[list[list], str]:
    return_tensor = deepcopy(tensor)
    return_tensor[final[0]][final[1]][1] = tensor[origin[0]][origin[1]][1]
    return_tensor[origin[0]][origin[1]][1] = None
    return return_tensor, return_tensor[final[0]][final[1]][0]


def is_won(current_soldier_position: tuple[int, int], team_color: constants.SoldierColor) -> bool:
    if team_color is constants.SoldierColor.LIGHT:
        if current_soldier_position[0] == 7:
            return True
        return False
    else:
        if current_soldier_position[0] == 0:
            return True
        return False

def tensor_print(tensor: list[list]):
    for covector in tensor:
        print(covector)
    print("\n\n\n")
