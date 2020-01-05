from game_board import *


def swap_player(old_player):
    if old_player == TicTacToeCell.O:
        return TicTacToeCell.X
    else:
        return TicTacToeCell.O


def split_input(user_input):
    splited = user_input.split(",")
    return int(splited[0]) , int(splited[1])


tic_tac_toe_game = TicTacToeGameBoard()
current_player = TicTacToeCell.O

while True:
    tic_tac_toe_game.print_game()
    i, j = split_input(input())
    try:
        tic_tac_toe_game.place_chess(i, j, current_player)

    except Exception as e:
        print(e)
        break
    current_player = swap_player(current_player)
