from copy import deepcopy

from tic_tac_toe_min_max_tree import *


class TicTacToeAi:
    def __init__(self, board: TicTacToeGameBoard, player: TicTacToeCell):
        self._board = board
        self._player = player

    def set_board(self, board: TicTacToeGameBoard):
        self._board = board

    def get_board(self) -> TicTacToeGameBoard:
        return self._board

    def place_chess(self):
        pass


class TicTacToeMinMaxTreeAi(TicTacToeAi):
    def __init__(self, board: TicTacToeGameBoard, player: TicTacToeCell):
        super().__init__(board, player)
        self._min_max_tree = None

    def generate_min_max_tree(self):
        if self._min_max_tree is None:
            self._min_max_tree = TicTacToeTreeNode(self.get_board())
            get_game_tree(self._min_max_tree)

    def set_min_max_tree(self, tree: TicTacToeTreeNode):
        self._min_max_tree = tree

    def find_position(self, board: TicTacToeGameBoard):
        self._min_max_tree = get_node_from_game_tree(board, self._min_max_tree)

    def place_chess(self):
        self._min_max_tree = AI_place_chess(self._min_max_tree,self._player)
        self._board = deepcopy(self._min_max_tree.tic_tac_toe_game)

