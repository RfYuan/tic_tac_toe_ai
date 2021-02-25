from typing import List

from game_board import TicTacToeCell


# This util assume game_board

def check_win(game_board: List) -> TicTacToeCell:
    game_board = to_matrix_3(game_board)
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2]:
            return game_board[i][0]

        elif game_board[0][i] == game_board[1][i] == game_board[2][i]:
            return game_board[0][i]

    if game_board[0][0] == game_board[1][1] == game_board[2][2] or \
            game_board[0][2] == game_board[1][1] == game_board[2][0]:
        return game_board[1][1]
    return TicTacToeCell.N


def to_matrix_3(l):
    return [l[0:3], l[3:6], l[6:9]]


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def print_game(game_board):
    matrix = to_matrix(game_board, 3)
    for i in range(3):
        print(''.join([x.name for x in matrix[i]]))
    print()


def get_possible_move(game_board):
    result = []
    for i in range(9):
        if game_board[i] == TicTacToeCell.N:
            result.append((i))
    return result


class MixMaxTreeNode:

    # finished = None
    def __init__(self):
        self.childrens = []
        self.parent = []
        self.score = None

    def set_childrens(self, childrens):
        self.childrens = childrens

    def set_parent(self, parent):
        self.parent = parent

    def is_finished(self):
        pass

    def _test_finish(self):
        pass


class TicTacToeGameBoard:

    def __init__(self, board=None):
        if board is None:
            self.board = [TicTacToeCell.N] * 9
        else:
            self.board = board
        self.winner = TicTacToeCell.N
        self.finished = False

    def _test_finish(self):
        self.winner = check_win(self.board)
        if self.turn_played() == 9:
            self.finished = True
        elif self.winner != TicTacToeCell.N and self.winner != TicTacToeCell.N.value:
            self.finished = True
        else:
            self.finished = False

    def is_finished(self):
        self._test_finish()
        return self.finished


    def __hash__(self) -> int:
        return hash(self.board)

    def __eq__(self, other):
        if isinstance(other, TicTacToeGameBoard):
            return self.board == other.board
        else:
            return False

    def turn_played(self):
        return len([x for x in self.board if x != TicTacToeCell.N])

    def __le__(self, other):
        return self.turn_played() <= other.turn_played()

    def __lt__(self, other):
        return self.turn_played() < other.turn_played()

    def print_game(self):
        print_game(self.board)


class TicTacToeTreeNode(MixMaxTreeNode):

    def __init__(self, tic_tac_toe_game=None):
        super().__init__()
        if tic_tac_toe_game is None:
            self.tic_tac_toe_game = None
        else:
            self.tic_tac_toe_game = tic_tac_toe_game

    def __hash__(self) -> int:
        return self.tic_tac_toe_game.__hash__()

    def __eq__(self, o: object) -> bool:
        if isinstance(o, TicTacToeTreeNode):
            return self.tic_tac_toe_game.board == o.tic_tac_toe_game.board
        else:
            return False
