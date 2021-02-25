import enum


class TicTacToeCell(enum.Enum):
    N = 0
    O = 1
    X = 2


class InvalidMoveError(RuntimeError):
    pass


class GameFinished(RuntimeError):
    pass


class TicTacToeGameBoard:
    winner = TicTacToeCell.N
    finished = False

    def __init__(self):
        self.game_board = [x[:] for x in [[TicTacToeCell.N] * 3] * 3]

    def _place_chess(self, i, j, player):
        if (self.game_board[i][j] != TicTacToeCell.N) or (i < 0) or (i > 2) or (j < 0) or (j > 2):
            raise InvalidMoveError
        else:
            self.game_board[i][j] = player

    def _check_win(self):
        for i in range(3):
            if self.game_board[i][0] == self.game_board[i][1] == self.game_board[i][2]:
                self.winner = self.game_board[i][0]
                break
            elif self.game_board[0][i] == self.game_board[1][i] == self.game_board[2][i]:
                self.winner = self.game_board[0][i]
                break

        if self.game_board[0][0] == self.game_board[1][1] == self.game_board[2][2] or \
                self.game_board[0][2] == self.game_board[1][1] == self.game_board[2][0]:
            self.winner = self.game_board[1][1]

    def check_win(self):
        self._check_win()
        if self.winner != TicTacToeCell.N:
            self.finished = True
            raise GameFinished("Gmae finished with " + self.winner.name + " win")

    def place_chess(self, i, j, player):
        if self.finished:
            raise InvalidMoveError("Gmae already finished with " + self.winner.name + " win")
        else:
            self._place_chess(i, j, player)
            self.check_win()

    def set_game(self, current_game_state):
        self.game_board = current_game_state

    def print_game(self):
        for i in range(3):
            print(' '.join([x.name for x in self.game_board[i]]))

    def __eq__(self, other):
        if isinstance(other, TicTacToeGameBoard):
            return self.get_flattened_game() == other.get_flattened_game()
        else:
            return False

    def turn_played(self):
        return len([x for x in self.get_flattened_game() if x != TicTacToeCell.N])

    def get_flattened_game(self):
        return [item for sublist in self.game_board for item in sublist]

    def __hash__(self) -> int:
        return hash(tuple(self.get_flattened_game()))

    def __le__(self, other):
        return self.turn_played() <= other.turn_played()

    def __lt__(self, other):
        return self.turn_played() < other.turn_played()
