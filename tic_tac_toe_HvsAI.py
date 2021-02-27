from copy import deepcopy

import tic_tac_toe_min_max_tree as min_max_tree_util
from tic_tac_toe_util import *
from tic_tac_toe_ai import TicTacToeMinMaxTreeAi

def swap_player(old_player):
    if old_player == TicTacToeCell.O:
        return TicTacToeCell.X
    else:
        return TicTacToeCell.O


def split_input(user_input):
    splited = user_input.split(",")
    i,j = int(splited[0]), int(splited[1])
    assert 0<=i and i<=2 and 0<=j and j<=2
    return i,j


def place_chess(game, position, user):
    game.board[position] = user


def input_until_valid_move():
    i, j = None, None
    while True:
        try:
            i, j = split_input(input("Please enter your move: "))
        except Exception or ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            break
    return i, j


tic_tac_toe_game = TicTacToeGameBoard()
player_turn = TicTacToeCell.O

min_max_ai = None

# User first
while True:
    tic_tac_toe_game.print_game()
    i, j = input_until_valid_move()
    place_chess(tic_tac_toe_game, i * 3 + j, player_turn)
    if tic_tac_toe_game.is_finished():
        if tic_tac_toe_game.winner == player_turn:
            print("You win!!!")
        exit(0)

    tic_tac_toe_game.print_game()

    if min_max_ai  is None:
        min_max_ai = TicTacToeMinMaxTreeAi(tic_tac_toe_game,TicTacToeCell.X)
        min_max_ai.generate_min_max_tree()
        # min_max_ai.find_position()
        # min_max_tree_util.get_game_tree(current_node)
    else:
        min_max_ai.find_position(tic_tac_toe_game.board)

    min_max_ai.place_chess()
    # current_node = min_max_tree_util.AI_place_chess(current_node, TicTacToeCell.X)
    tic_tac_toe_game = deepcopy(min_max_ai.get_board())

    if tic_tac_toe_game.is_finished():
        tic_tac_toe_game.print_game()
        print("Ai win!!!")
        exit(0)
