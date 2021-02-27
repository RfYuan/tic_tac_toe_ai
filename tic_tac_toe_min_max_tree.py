import logging
import sys
import threading
import time

from tic_tac_toe_util import *

# print(resource.getrlimit(resource.RLIMIT_STACK))

MIN_MAX_TREE_TTT_GAME_SAVE_FILE = 'tic_tac_toe_game_tree'


# TicTacToeCell.O would be the first move player and score 1 if win
# TicTacToeCell.X would be the second move player and score 0 if win

def get_game_tree(game_tree_node: TicTacToeTreeNode):
    t0 = time.time()
    generate_childrens(game_tree_node)
    t1 = time.time()
    print("generated_all_nodes", t1 - t0)
    # tmp_node = game_tree_node.childrens[0]
    scores_tree_node(game_tree_node)
    t2 = time.time()
    print("score_nodes", t2 - t1)


def AI_place_chess(min_max_tree, player):
    if player == TicTacToeCell.O:
        next_game_node = find_max_from_tree(min_max_tree)
    else:
        next_game_node = find_min_from_tree(min_max_tree)
    return next_game_node


def find_max_from_tree(game_tree_node: TicTacToeTreeNode):
    assert len(game_tree_node.childrens) > 0
    childrens = game_tree_node.childrens
    max_node = childrens[0]
    for i in childrens:
        if i.score > max_node.score:
            max_node = i
    return max_node


def find_min_from_tree(game_tree_node: TicTacToeTreeNode):
    assert len(game_tree_node.childrens) > 0
    childrens = game_tree_node.childrens
    min_node = childrens[0]
    for i in childrens:
        if i.score < min_node.score:
            min_node = i
    return min_node


def get_node_from_game_tree(board:TicTacToeGameBoard, gameTreeNode: TicTacToeTreeNode):
    unviewed = [gameTreeNode]
    while len(unviewed) > 0:
        current_node = unviewed.pop()
        if current_node.tic_tac_toe_game.board == board:
            return current_node
        unviewed += current_node.childrens
    logging.error("could find tree node for " + str(board))
    raise RuntimeError("could find tree node for " + str(board.board))


def generate_childrens(game_tree_node: TicTacToeTreeNode):
    unviewed = [game_tree_node]
    seen_nodes = []
    while len(unviewed) > 0:
        # print(len(unviewed), len(seen_nodes))
        current_considered = unviewed.pop(0)
        game = current_considered.tic_tac_toe_game
        if current_considered in seen_nodes:
            continue
        seen_nodes.append(current_considered)
        # seen_nodes.append(game.board)
        if not game.is_finished():
            player = get_current_player(game)
            possible_moves = get_possible_move(game.board)
            for i in possible_moves:
                tmp_game = place_chess(game, i, player)
                new_node = TicTacToeTreeNode(tmp_game)
                if new_node in seen_nodes:
                    # this never happened because we are width first search
                    existed_node_index = seen_nodes.index(new_node)
                    current_considered.childrens.append(seen_nodes[existed_node_index])
                    seen_nodes[existed_node_index].parent.append(current_considered)
                elif new_node in unviewed:
                    existed_node_index = unviewed.index(new_node)
                    current_considered.childrens.append(unviewed[existed_node_index])
                    unviewed[existed_node_index].parent.append(current_considered)
                else:
                    current_considered.childrens.append(new_node)
                    new_node.parent.append(current_considered)
                    unviewed.append(new_node)
    print(len(seen_nodes))


def place_chess(game: TicTacToeGameBoard, pos, current_player):
    tmp = game.board.copy()
    tmp[pos] = current_player
    game = TicTacToeGameBoard(board=tmp)
    return game


def get_current_player(ttt_game: TicTacToeGameBoard):
    if ttt_game.turn_played() % 2 == 0:
        return TicTacToeCell.O
    else:
        return TicTacToeCell.X


def scores_tree_node(game_tree_node: TicTacToeTreeNode):
    if game_tree_node.score is not None:
        return
    game = game_tree_node.tic_tac_toe_game
    player = "min" if game.turn_played() % 2 == 1 else "max"

    if game.is_finished():
        if game.winner == TicTacToeCell.O:
            game_tree_node.score = 1
        elif game.winner == TicTacToeCell.N:
            game_tree_node.score = 0.5
        else:
            game_tree_node.score = 0
    else:
        childrens = game_tree_node.childrens

        childrens_scores = []
        for node in childrens:
            scores_tree_node(node)
            childrens_scores.append(node.score)

        if player == "min":
            game_tree_node.score = min(childrens_scores)
        else:
            game_tree_node.score = max(childrens_scores)


if __name__ == "__main__":
    threading.stack_size(20000000)
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(100000)
    a, b, c = TicTacToeCell.N, TicTacToeCell.O, TicTacToeCell.X
    # empty_game = TicTacToeGameBoard(board=[b,c,b,a,a,c,a,a,a])
    # empty_game = TicTacToeGameBoard(board=[b,c,c,b,a,a,a,a,a])
    # empty_game = TicTacToeGameBoard(board=[b,a,a,a,a,a,a,a,a])
    empty_game = TicTacToeGameBoard(board=[a, a, a, a, a, a, a, a, a])
    empty_game_node = TicTacToeTreeNode(empty_game)
    get_game_tree(empty_game_node)

    # with open(MIN_MAX_TREE_TTT_GAME_SAVE_FILE, 'wb') as file:
    #     thread = threading.Thread(pickle.dump(empty_game_node, file))
    #     thread.start()

    # for i in empty_game_node.childrens:
    #     print_game(i.tic_tac_toe_game.board)
