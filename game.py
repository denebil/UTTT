import sys
import random


class GameState(object):

    def __init__(self):
        self.possible_moves = [(i, j) for i in range(3) for j in range(3)]
        self.board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        self.last_move = None
        self.player_to_move = 0
        self.previous_player = 1
        self.moves_count = 0
        self.is_game_finished = False
        self.winner = 2  # 0,1 - winner; 2 - draw

    def make_move(self, column, row):
        if self.is_game_finished:
            print("Invalid move - game already finished", file=sys.stderr)
            return
        if self.board[row][column] != 2:
            print("Invalid move - square ({0},{1}) occupied", column, row, file=sys.stderr)
            return

        self.board[row][column] = self.player_to_move
        self.switch_player_to_move()
        self.last_move = (column, row)
        self.moves_count += 1
        self.check_winner()
        self.possible_moves.remove((column, row))
        if not self.possible_moves:
            if not self.is_game_finished:
                self.set_winner(2)

    def switch_player_to_move(self):
        temp_player = self.player_to_move
        self.player_to_move = self.previous_player
        self.previous_player = temp_player

    def check_winner(self):
        if self.last_move is None:
            return
        self.check_row(self.last_move[1])
        self.check_column(self.last_move[0])
        self.check_diagonal(self.last_move)
        if not self.is_game_finished:
            if not self.possible_moves:
                self.set_winner(2)

    def check_row(self, row):
        if 2 not in self.board[row] and self.player_to_move not in self.board[row]:
            self.set_winner(self.previous_player)

    def check_column(self, column):
        column_content = [self.board[0][column], self.board[1][column], self.board[2][column]]
        if 2 not in column_content and self.player_to_move not in column_content:
            self.set_winner(self.previous_player)

    def check_diagonal(self, square):
        row, column = square
        if row == column:
            diagonal = [self.board[x][x] for x in range(3)]
            if 2 not in diagonal and self.player_to_move not in diagonal:
                self.set_winner(self.previous_player)
                return
        if row + column == 2:
            diagonal = [self.board[x][2 - x] for x in range(3)]
            if 2 not in diagonal and self.player_to_move not in diagonal:
                self.set_winner(self.previous_player)

    def set_winner(self, winner):
        self.winner = winner
        self.is_game_finished = True

    def is_finished(self):
        return self.is_game_finished

    def get_result(self):
        if self.is_game_finished:
            return self.winner
        return None

    def __str__(self):
        return str(self.board)

    def simulate(self):
        while not self.is_game_finished:
            self.make_move(random.choice(range(3)))
        return self.winner


# while True:
#     opponent_row, opponent_col = [int(i) for i in input().split()]
#     valid_action_count = int(input())
#     for i in range(valid_action_count):
#         row, col = [int(j) for j in input().split()]

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# print("0 0")


# GameState diagonal test:
# g = GameState()
# g.make_move(0, 0)
# g.make_move(1, 0)
# g.make_move(1, 1)
# g.make_move(2, 1)
# g.make_move(2, 2)
