import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop

moves = [(i, j) for i in range(3) for j in range(3)]


class GameState(object):
    board = []
    player_to_move = 0
    previous_player = 1
    winner = False
    last_move = None
    possible_moves = []
    moves_count = 0

    def __init__(self):
        self.board = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
        self.player_to_move = 0
        self.previous_player = 1
        self.moves_count = 0
        self.possible_moves = moves
        self.winner = False

    def make_move(self, column, row):
        if self.board[column][row] != 2:
            print("Invalid move", file=sys.stderr)
        else:
            self.board[column][row] = self.player_to_move
            temp_player = self.player_to_move
            self.player_to_move = self.previous_player
            self.previous_player = temp_player
            self.last_move = (column, row)
            self.moves_count += 1
            self.winner = self.check_winner()
            moves.remove((column, row))

    def check_winner(self):
        if self.last_move is None:
            return False
        if self.possible_moves:
            self.winner = 2
            return
        check_row(self.last_move[1])
        check_column(self.last_move[0])

    def check_column(self, column):
        if 2 in [self.board[column][0], self.board[column][1], self.board[column][2]]:
            self.winner = False
            return
        if self.player_to_move in [self.board[column][0], self.board[column][1], self.board[column][2]]:
            self.winner = False
            return
        self.winner = self.previous_player

    def check_row(self, row):
        if 2 in self.board[row]:
            self.winner = False
            return
        if self.player_to_move in self.board[row]:
            self.winner = False
            return
        self.winner = self.previous_player

    def __str__(self):
        return str(self.board)


while True:
    opponent_row, opponent_col = [int(i) for i in input().split()]
    valid_action_count = int(input())
    for i in range(valid_action_count):
        row, col = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    print("0 0")