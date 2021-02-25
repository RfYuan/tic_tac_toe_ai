from game_board import *

empty_game = TicTacToeGameBoard()
states = {empty_game}
change = True
unviewed = [empty_game]


def get_current_player(ttt_game):
    if ttt_game.turn_played() % 2 == 0:
        return TicTacToeCell.O
    else:
        return TicTacToeCell.X


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def print_flattened(falttened):
    matrix = to_matrix(falttened,3)
    for i in range(3):
        print(''.join([x.name for x in matrix[i]]))

def place_chess(flattened, pos):
    flattened = flattened.copy()
    flattened[pos] = current_player
    next_game_matrix = to_matrix(flattened, 3)
    game = TicTacToeGameBoard()
    game.set_game(next_game_matrix)
    return game


while len(unviewed) > 0:
    current_considered = unviewed.pop(0)
    if not (current_considered.finished):
        current_game_flatten = current_considered.get_flattened_game()
        current_player = get_current_player(current_considered)
        # print_flattened(current_game_flatten)
        # print()
        for i in range(9):
            if current_game_flatten[i] == TicTacToeCell.N:
                try:
                    next_game = place_chess(current_game_flatten, i)
                    if next_game not in states:
                        states.add(next_game)
                        unviewed.append(next_game)
                    next_game.check_win()
                except:
                    pass

print(len(states))