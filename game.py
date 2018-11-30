import sys
import gc
from random import choice
from copy import deepcopy
from math import log, sqrt
import time


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

    def get_possible_moves(self):
        if self.is_game_finished:
            return None
        return self.possible_moves

    def __str__(self):
        return str(self.board)


class MCNode(object):
    player_to_simulate = 0
    time_margin = 0.02
    C = 0.5

    def __init__(self, move, parent):
        self.parent = parent
        if parent:
            self.game_state = deepcopy(parent.game_state)
        else:
            self.game_state = GameState()

        if move:
            self.game_state.make_move(move[0], move[1])

        self.unvisited_children = deepcopy(self.game_state.get_possible_moves())
        self.win_count = 0
        self.simulation_count = 0
        self.visited_children = []

    def search(self, time_per_move):  # time in ms (1000000 ns)
        time_margin = self.time_margin * time_per_move
        time_start = time.process_time()  # self.time_margin
        # if len(self.game_state.get_possible_moves()) == 1:
        #     return self.game_state.get_possible_moves()[0]
        # else:
        while time.process_time() - time_start < time_per_move - time_margin:
                # visit
            self.visit()
        # return self.get_the_best_node()
        return self.get_the_most_visited_node()

    def visit(self):
        if self.unvisited_children:
            # expand
            move = choice(self.unvisited_children)
            self.unvisited_children.remove(move)
            new_node = MCNode(move, self)
            self.visited_children.append(new_node)
            # sim new node
            new_node.sim()
        else:
            # if game is finished run sim
            if self.game_state.is_game_finished:
                self.sim()
            # visit best move
            else:
                self.get_the_best_node().visit()

    def uct(self, node):
        if self.player_to_simulate == self.game_state.player_to_move:
            relative_wins = node.win_count
        else:
            relative_wins = node.simulation_count - node.win_count

        return relative_wins / node.simulation_count + self.C * sqrt(
            log(self.simulation_count) / node.simulation_count)

    def get_the_best_node(self):
        return max(self.visited_children, key=self.uct)

    def get_the_most_visited_node(self):
        return max(self.visited_children, key=lambda x: x.simulation_count)

    def sim(self):
        # sim
        sim_game_state = deepcopy(self.game_state)
        while not sim_game_state.is_finished():
            move = choice(sim_game_state.get_possible_moves())
            sim_game_state.make_move(move[0], move[1])
        # back_prop
        result = sim_game_state.get_result()
        score = 0
        if result == 2:
            score = 0.5
        elif result == self.player_to_simulate:
            score = 1
        self.back_propagate(score)

    def back_propagate(self, score):
        self.simulation_count += 1
        self.win_count += score
        if self.parent:
            self.parent.back_propagate(score)


gc.disable()
first_round_time = 1
round_time = 0.1
round_count = 1

while True:

    opponent_row, opponent_col = [int(i) for i in input().split()]
    for i in range(int(input())):
        input()
    if round_count == 1:
        tree = MCNode(None, None)
        time_left = first_round_time
        if (opponent_row, opponent_col) == (-1, -1):
            tree.player_to_simulate = 0
        else:
            tree.player_to_simulate = 1
            tree.game_state.make_move(opponent_col, opponent_row)
    else:
        time_left = round_time

        new_tree = next((node for node in tree.visited_children if node.game_state.last_move == (opponent_col, opponent_row)), None)
        if not new_tree:
            new_tree = MCNode((opponent_col, opponent_row), tree)

        tree = new_tree
        tree.parent = None

    node_to_go = tree.search(time_left)
    move = node_to_go.game_state.last_move
    print("State:", tree.game_state.board, file=sys.stderr)
    print("Last move:", tree.game_state.last_move, file=sys.stderr)
    print("moves left:", tree.game_state.get_possible_moves(), file=sys.stderr)
    print("Sim count:", tree.simulation_count, file=sys.stderr)
    print("Move found:", node_to_go.game_state.last_move, file=sys.stderr)
    print(move[1], move[0])
    tree = node_to_go
    print("State after:", tree.game_state.board, file=sys.stderr)
    tree.parent = None
    round_count += 1

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
