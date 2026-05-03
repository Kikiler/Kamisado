from enum import StrEnum

NAME_TAG = "roofdier"
MATRICULE = 24330
RECEPTION_PORT = 4000
COMMUNICATION_PORT = 3000
GAME_HOSTING_IP_ADDRESS = "172.17.10.125"
MY_IP = "0.0.0.0"

static_dangerosity_tensor_white = [[8, 8, 8, 8, 8, 8, 8, 8],
                                   [7, 8, 8, 8, 8, 8, 8, 7],
                                   [6, 7, 8, 8, 8, 8, 7, 6],
                                   [5, 6, 7, 8, 8, 7, 6, 5],
                                   [4, 5, 6, 7, 7, 6, 5, 4],
                                   [3, 4, 5, 5, 5, 5, 4, 3],
                                   [2, 3, 4, 4, 4, 4, 3, 2],
                                   [-1, -1, -1, -1, -1, -1, -1, -1]
                                   ]

static_dangerosity_tensor_black = static_dangerosity_tensor_white[::-1]


class SoldierColor(StrEnum):
    DARK = "dark"
    LIGHT = "light"
