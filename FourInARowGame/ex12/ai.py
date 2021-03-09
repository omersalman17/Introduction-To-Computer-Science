import random

COL_NUM = 7


class AI:

    def __init__(self, game, player):
        self.__player = player
        self.__game = game

    def find_legal_move(self, timeout=None):
        if self.__game.get_winner() is not None:
            raise Exception("No possible AI moves")
        if self.__game.get_current_player() != self.__player:
            raise Exception("Wrong player")
        col = random.randint(0, COL_NUM)
        for delta in range(COL_NUM):
            column = (col + delta) % COL_NUM
            if self.__game.get_player_at(0, column) is None:
                return column
        raise Exception("No possible AI moves")

    def get_last_found_move(self):
        pass
