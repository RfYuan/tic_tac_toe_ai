from copy import deepcopy

import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from sklearn.preprocessing import OneHotEncoder

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
        self._min_max_tree = AI_place_chess(self._min_max_tree, self._player)
        self._board = deepcopy(self._min_max_tree.tic_tac_toe_game)


def generate_NN_model():
    model = Sequential()
    model.add(Dense(32, input_dim=9, activation='relu'))
    model.add(Dense(256, activation='relu'))
    # model.add(Dense(1024, activation='relu'))
    # model.add(Dense(256, activation='relu'))
    # model.add(Dense(128, activation='relu'))
    # model.add(Dense(9, activation='softmax'))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss="mse", metrics=["mae"],
                  optimizer=Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-7))
    # model.compile(loss="mse", metrics=["mae"], optimizer="Adam")
    return model


class TicTacToeNNAi(TicTacToeAi):
    def __init__(self, board: TicTacToeGameBoard, player: TicTacToeCell):
        super().__init__(board, player)
        self._NN_model = generate_NN_model()


def train_ttt_ai():
    empty_board = TicTacToeGameBoard()
    empty_game_node = TicTacToeTreeNode(empty_board)
    get_game_tree(empty_game_node)
    game_board_list, score_list = get_board_and_score_from_game_tree_node(empty_game_node)
    nn_ai_model = generate_NN_model()
    X = np.asarray(game_board_list)
    original_y = np.vstack(np.asarray(score_list))
    encoder = OneHotEncoder(categories='auto')
    # categorical_y = to_categorical(original_y)
    categorical_y = encoder.fit_transform(original_y)
    print(X.shape)
    print(categorical_y.shape)

    es = EarlyStopping(monitor='loss', verbose=2, patience=20)
    history = nn_ai_model.fit(x=X, y=categorical_y, verbose=2, epochs=300, callbacks=[es])
    return nn_ai_model, history


if __name__ == "__main__":
    start = time.time()
    my_model, history = train_ttt_ai()
    end = time.time()
    print("total running time {}".format(start - end))
