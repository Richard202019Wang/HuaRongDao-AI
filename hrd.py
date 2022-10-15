# The assignment follows the handout steps on quercus.


import copy
import sys


class BoardState:
    def __init__(self, board_state, last_board=None):
        # Implement a data structure to store a state.
        # board_state is the current board state and the last_board represents its parent and the default value is None.
        self.board_state = copy.deepcopy(board_state)
        # deepcopy to avoid ignoring other boards.
        self.last_board = last_board
        # cost of each step
        if self.last_board is None:
            self.cost = 0
        else:
            self.cost = last_board.cost + 1


class PriorityQ:
    # Implement a priority queue to store the frontier.
    def __init__(self):
        self.queue = []
        self.key = float("inf")
        self.value = None

    def put(self, key, value):
        self.queue.append([key, value])

    def is_empty(self):
        if self.queue:
            return False
        else:
            return True

    def pop(self):
        result_que = self.queue[0]
        for i in self.queue:
            if result_que[0] > i[0]:
                result_que = i
        self.queue.remove(result_que)
        return result_que


def read_inputfile():
    # read the initial board from the input file
    aim_file = open(sys.argv[1], "r")
    initial_state = BoardState([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    current_line = 0
    while current_line < 5:
        current_char = 0
        read_line = aim_file.readline()
        while current_char < 4:
            initial_state.board_state[current_line][current_char] = int(read_line[current_char])
            current_char += 1
        current_line += 1
    aim_file.close()
    return initial_state


def convert_state(boardstate):
    # convert the input file format number to match the output file format number
    final_state = ""
    current_line = 0
    while current_line < 5:
        current_char = 0
        while current_char < 4:
            cur = boardstate.board_state[current_line][current_char]
            if boardstate.board_state[current_line][current_char] == 7:
                final_state += "4"
            elif boardstate.board_state[current_line][current_char] == 1:
                final_state += "1"
            elif boardstate.board_state[current_line][current_char] == 0:
                final_state += "0"
            elif current_char + 1 < 4 and boardstate.board_state[current_line][current_char + 1] == cur:
                final_state += "2"
                final_state += "2"
                current_char += 1
            else:
                final_state += "3"
            current_char += 1
        final_state += "\n"
        current_line += 1
    final_state += "\n"
    return final_state


def if_reach_goal(boardstate):
    # Algorithm to judge if caocao reaches the goal.
    if boardstate.board_state[3][1] == 1 and boardstate.board_state[4][2] == 1:
        return True
    else:
        return False


def empty_position(boardstate):
    # Get the empty grids position and stored into a list in order to judge if a block can move or not
    empty_grid = []
    current_line = 0
    while current_line < 5:
        current_char = 0
        while current_char < 4:
            if boardstate.board_state[current_line][current_char] == 0:
                empty_grid += [current_line]
                empty_grid += [current_char]
            current_char += 1
        current_line += 1

    return empty_grid


# Below are the algorithm to test if the single block can move or not in four directions
def single_up_move(boardstate, empty_grid):
    successors_list = []
    if empty_grid[0] < 4 and boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = 7
        successor.board_state[empty_grid[0] + 1][empty_grid[1]] = 0
        successors_list += [successor]
    if empty_grid[2] < 4 and boardstate.board_state[empty_grid[2] + 1][empty_grid[3]] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[2]][empty_grid[3]] = 7
        successor.board_state[empty_grid[2] + 1][empty_grid[3]] = 0
        successors_list += [successor]
    return successors_list


def single_down_move(boardstate, empty_grid):
    successors_list = []
    if empty_grid[0] > 0 and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = 7
        successor.board_state[empty_grid[0] - 1][empty_grid[1]] = 0
        successors_list += [successor]
    if empty_grid[2] > 0 and boardstate.board_state[empty_grid[2] - 1][empty_grid[3]] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[2]][empty_grid[3]] = 7
        successor.board_state[empty_grid[2] - 1][empty_grid[3]] = 0
        successors_list += [successor]
    return successors_list


def single_left_move(boardstate, empty_grid):
    successors_list = []
    if empty_grid[1] < 3 and boardstate.board_state[empty_grid[0]][empty_grid[1] + 1] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = 7
        successor.board_state[empty_grid[0]][empty_grid[1] + 1] = 0
        successors_list += [successor]
    if empty_grid[3] < 3 and boardstate.board_state[empty_grid[2]][empty_grid[3] + 1] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[2]][empty_grid[3]] = 7
        successor.board_state[empty_grid[2]][empty_grid[3] + 1] = 0
        successors_list += [successor]
    return successors_list


def single_right_move(boardstate, empty_grid):
    successors_list = []
    if empty_grid[1] > 0 and boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = 7
        successor.board_state[empty_grid[0]][empty_grid[1] - 1] = 0
        successors_list += [successor]

    if empty_grid[3] > 0 and boardstate.board_state[empty_grid[2]][empty_grid[3] - 1] == 7:
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[2]][empty_grid[3]] = 7
        successor.board_state[empty_grid[2]][empty_grid[3] - 1] = 0
        successors_list += [successor]
    return successors_list


# Below are the 1*2 or 2*1 or 2*2 blocks movement justification for the up direction
def horizontal_up(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] < 4 and empty_grid[0] == empty_grid[2]
            and boardstate.board_state[empty_grid[0] + 1][empty_grid[1]]
            == boardstate.board_state[empty_grid[2] + 1][empty_grid[3]] and abs(empty_grid[3] - empty_grid[1]) == 1):
        if (boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] != 1
                and boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0] + 1][
                empty_grid[1]]
            successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2] + 1][
                empty_grid[3]]
            successor.board_state[empty_grid[0] + 1][empty_grid[1]] = 0
            successor.board_state[empty_grid[2] + 1][empty_grid[3]] = 0
            successors_list += [successor]
    return successors_list


def caocao_up(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] < 3 and empty_grid[0] == empty_grid[2]
            and abs(empty_grid[3] - empty_grid[1]) == 1):
        if (boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] == 1
                and boardstate.board_state[empty_grid[2] + 1][empty_grid[3]] == 1):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = 1
            successor.board_state[empty_grid[2]][empty_grid[3]] = 1
            successor.board_state[empty_grid[0] + 2][empty_grid[1]] = 0
            successor.board_state[empty_grid[2] + 2][empty_grid[3]] = 0
            successors_list += [successor]
    return successors_list


def vertical_up(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] < 3 and boardstate.board_state[empty_grid[0] + 1][empty_grid[1]]
            == boardstate.board_state[empty_grid[0] + 2][empty_grid[1]]):
        if (boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] != 1
                and boardstate.board_state[empty_grid[0] + 1][empty_grid[1]] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0] + 1][empty_grid[1]]
            successor.board_state[empty_grid[0] + 2][empty_grid[1]] = 0
            successors_list += [successor]
    if empty_grid[2] < 3:
        if (boardstate.board_state[empty_grid[2] + 1][empty_grid[3]]
                == boardstate.board_state[empty_grid[2] + 2][empty_grid[3]]
                and boardstate.board_state[empty_grid[2] + 1][empty_grid[3]] != 1
                and boardstate.board_state[empty_grid[2] + 1][empty_grid[3]] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2] + 1][empty_grid[3]]
            successor.board_state[empty_grid[2] + 2][empty_grid[3]] = 0
            successors_list += [successor]

    return successors_list


# Below are the 1*2 or 2*1 or 2*2 blocks movement justification for the down direction
def horizontal_down(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] > 0 and empty_grid[0] == empty_grid[2]
            and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]]
            == boardstate.board_state[empty_grid[2] - 1][empty_grid[3]] and abs(empty_grid[3] - empty_grid[1]) == 1):
        if (boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] != 1
                and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0] - 1][
                empty_grid[1]]
            successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2] - 1][
                empty_grid[3]]
            successor.board_state[empty_grid[0] - 1][empty_grid[1]] = 0
            successor.board_state[empty_grid[2] - 1][empty_grid[3]] = 0
            successors_list += [successor]
    return successors_list


def caocao_down(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] > 1 and empty_grid[0] == empty_grid[2] and boardstate.board_state[empty_grid[0] - 1][
        empty_grid[1]] == boardstate.board_state[empty_grid[2] - 1][empty_grid[3]]
            and abs(empty_grid[3] - empty_grid[1]) == 1
            and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] == 1):
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = 1
        successor.board_state[empty_grid[2]][empty_grid[3]] = 1
        successor.board_state[empty_grid[0] - 2][empty_grid[1]] = 0
        successor.board_state[empty_grid[2] - 2][empty_grid[3]] = 0
        successors_list += [successor]
    return successors_list


def vertical_down(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[0] > 1 and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] != 1
        and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]] != 7
            and boardstate.board_state[empty_grid[0] - 1][empty_grid[1]]
            == boardstate.board_state[empty_grid[0] - 2][empty_grid[1]]):
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0] - 1][empty_grid[1]]
        successor.board_state[empty_grid[0] - 2][empty_grid[1]] = 0
        successors_list += [successor]
    if (empty_grid[2] > 1 and boardstate.board_state[empty_grid[2] - 1][empty_grid[3]] != 1
        and boardstate.board_state[empty_grid[2] - 1][empty_grid[3]] != 7
            and boardstate.board_state[empty_grid[2] - 1][empty_grid[3]]
            == boardstate.board_state[empty_grid[2] - 2][empty_grid[3]]):
        successor = BoardState(boardstate.board_state, boardstate)
        successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2] - 1][empty_grid[3]]
        successor.board_state[empty_grid[2] - 2][empty_grid[3]] = 0
        successors_list += [successor]

    return successors_list


# Below are the 1*2 or 2*1 or 2*2 blocks movement justification for the right direction
def horizontal_right(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] > 1 and boardstate.board_state[empty_grid[0]][empty_grid[1] - 1]
            == boardstate.board_state[empty_grid[0]][empty_grid[1] - 2]):
        if (boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] != 1
                and boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0]][
                empty_grid[1] - 1]
            successor.board_state[empty_grid[0]][empty_grid[1] - 2] = 0
            successors_list += [successor]
    if (empty_grid[3] > 1 and boardstate.board_state[empty_grid[2]][empty_grid[3] - 1]
            == boardstate.board_state[empty_grid[2]][empty_grid[3] - 2]):
        if (boardstate.board_state[empty_grid[2]][empty_grid[3] - 1] != 1
                and boardstate.board_state[empty_grid[2]][empty_grid[3] - 1] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2]][
                empty_grid[3] - 1]
            successor.board_state[empty_grid[2]][empty_grid[3] - 2] = 0
            successors_list += [successor]
    return successors_list


def caocao_right(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] > 1 and empty_grid[1] == empty_grid[3] and boardstate.board_state[empty_grid[0]][
        empty_grid[1] - 1] == boardstate.board_state[empty_grid[2]][empty_grid[3] - 1]
            and abs(empty_grid[2] - empty_grid[0]) == 1):
        if boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] == 1:
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = 1
            successor.board_state[empty_grid[2]][empty_grid[3]] = 1
            successor.board_state[empty_grid[0]][empty_grid[1] - 2] = 0
            successor.board_state[empty_grid[2]][empty_grid[3] - 2] = 0
            successors_list += [successor]
    return successors_list


def vertical_right(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] > 0 and empty_grid[1] == empty_grid[3] and boardstate.board_state[empty_grid[0]][
        empty_grid[1] - 1] == boardstate.board_state[empty_grid[2]][empty_grid[3] - 1]
            and abs(empty_grid[2] - empty_grid[0]) == 1):
        if boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] != 7 \
                and boardstate.board_state[empty_grid[0]][empty_grid[1] - 1] != 1:
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] =\
                boardstate.board_state[empty_grid[0]][empty_grid[1] - 1]
            successor.board_state[empty_grid[2]][empty_grid[3]] =\
                boardstate.board_state[empty_grid[0]][empty_grid[1] - 1]
            successor.board_state[empty_grid[0]][empty_grid[1] - 1] = 0
            successor.board_state[empty_grid[2]][empty_grid[3] - 1] = 0
            successors_list += [successor]

    return successors_list


# Below are the 1*2 or 2*1 or 2*2 blocks movement justification for the left direction
def horizontal_left(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] < 2 and boardstate.board_state[empty_grid[0]][empty_grid[1] + 1]
            == boardstate.board_state[empty_grid[0]][empty_grid[1] + 2]):
        if (boardstate.board_state[empty_grid[0]][empty_grid[1] + 1] != 1
                and boardstate.board_state[empty_grid[0]][empty_grid[1] + 2] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = boardstate.board_state[empty_grid[0]][
                empty_grid[1] + 1]
            successor.board_state[empty_grid[0]][empty_grid[1] + 2] = 0
            successors_list += [successor]
    if (empty_grid[3] < 2 and boardstate.board_state[empty_grid[2]][empty_grid[3] + 1]
            == boardstate.board_state[empty_grid[2]][empty_grid[3] + 2]):
        if (boardstate.board_state[empty_grid[2]][empty_grid[3] + 1] != 1
                and boardstate.board_state[empty_grid[2]][empty_grid[3] + 1] != 7):
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[2]][empty_grid[3]] = boardstate.board_state[empty_grid[2]][
                empty_grid[3] + 1]
            successor.board_state[empty_grid[2]][empty_grid[3] + 2] = 0
            successors_list += [successor]
    return successors_list


def caocao_left(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] < 2 and empty_grid[1] == empty_grid[3] and boardstate.board_state[empty_grid[0]][
        empty_grid[1] + 1] == boardstate.board_state[empty_grid[2]][empty_grid[3] + 1]
            and abs(empty_grid[2] - empty_grid[0]) == 1):
        if boardstate.board_state[empty_grid[0]][empty_grid[1] + 1] == 1:
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] = 1
            successor.board_state[empty_grid[2]][empty_grid[3]] = 1
            successor.board_state[empty_grid[0]][empty_grid[1] + 2] = 0
            successor.board_state[empty_grid[2]][empty_grid[3] + 2] = 0
            successors_list += [successor]
    return successors_list


def vertical_left(boardstate, empty_grid):
    successors_list = []
    if (empty_grid[1] < 3 and empty_grid[1] == empty_grid[3] and boardstate.board_state[empty_grid[0]][
        empty_grid[1] + 1] == boardstate.board_state[empty_grid[2]][empty_grid[3] + 1]
            and abs(empty_grid[2] - empty_grid[0]) == 1):
        if boardstate.board_state[empty_grid[0]][empty_grid[1] + 1] != 1 \
                and boardstate.board_state[empty_grid[0]][empty_grid[1] + 1] != 7:
            successor = BoardState(boardstate.board_state, boardstate)
            successor.board_state[empty_grid[0]][empty_grid[1]] \
                = boardstate.board_state[empty_grid[2]][empty_grid[3] + 1]
            successor.board_state[empty_grid[2]][empty_grid[3]] \
                = boardstate.board_state[empty_grid[2]][empty_grid[3] + 1]
            successor.board_state[empty_grid[0]][empty_grid[1] + 1] = 0
            successor.board_state[empty_grid[2]][empty_grid[3] + 1] = 0
            successors_list += [successor]
    return successors_list


# Implement a function which takes a state and returns a list of its successor states.
def successors_state(board_state):
    # get the position of empty grid
    empty_grid = empty_position(board_state)
    successors = []
    # Add all successor
    successors += caocao_up(board_state, empty_grid)
    successors += vertical_up(board_state, empty_grid)
    successors += single_up_move(board_state, empty_grid)
    successors += horizontal_up(board_state, empty_grid)
    successors += caocao_down(board_state, empty_grid)
    successors += vertical_down(board_state, empty_grid)
    successors += horizontal_down(board_state, empty_grid)
    successors += single_down_move(board_state, empty_grid)
    successors += caocao_right(board_state, empty_grid)
    successors += vertical_right(board_state, empty_grid)
    successors += single_right_move(board_state, empty_grid)
    successors += horizontal_right(board_state, empty_grid)
    successors += caocao_left(board_state, empty_grid)
    successors += vertical_left(board_state, empty_grid)
    successors += horizontal_left(board_state, empty_grid)
    successors += single_left_move(board_state, empty_grid)
    return successors


# Calculate the heuristic cost(Manhattan heuristic)
def h_cost(board_state):
    # locate caocao position and use the top left position to calculate the Manhattons distance
    caocao = []
    current_line = 0
    while current_line < 5:
        current_char = 0
        while current_char < 4:
            if board_state.board_state[current_line][current_char] == 1:
                caocao.append(current_line)
                caocao.append(current_char)
            current_char += 1
        current_line += 1
    h = abs(caocao[0] - 3) + abs(caocao[1] - 1)
    return h


# Calculate the heuristic cost designed by myself(The square of Manhattan heuristic)
def h_dominant_cost(board_state):
    # locate caocao position and use the top left position to calculate
    # the Manhattons distance and then square the value.
    caocao = []
    current_line = 0
    while current_line < 5:
        current_char = 0
        while current_char < 4:
            if board_state.board_state[current_line][current_char] == 1:
                caocao.append(current_line)
                caocao.append(current_char)
            current_char += 1
        current_line += 1
    h = (abs(caocao[0] - 3) + abs(caocao[1] - 1)) ** 2
    return h


# Calculate the cost of each step
def g(board_state):
    return board_state.cost


# Implement a function that takes a solution (i.e. a sequence of states) and returns the cost of the solution.
def f(board_state):
    total_cost = h_cost(board_state) + g(board_state)
    return total_cost


# Implement a function that takes a dominant solution (i.e. a sequence of states) and returns the cost of the solution.
def f_dominant(board_state):
    total_cost = h_dominant_cost(board_state) + g(board_state)
    return total_cost


# Implement a star algorithm which translates the pesudocode from the lecture ppt
def a_star_alg(initialized_board):
    # Create Priority Queue to pop the smallest f value move
    frontier = PriorityQ()
    frontier.put(f(initialized_board), initialized_board)
    explored = set()
    while not frontier.is_empty():
        curr = frontier.pop()[1]
        # check for pruning if not append into the expanded set
        if convert_state(curr) not in explored:
            explored.add(convert_state(curr))
            successors = successors_state(curr)
            # add the successor to frontier if it is not the goal else return the goal with cost
            for successor in successors:
                if if_reach_goal(successor):
                    return [successor, f(successor)]
                else:
                    frontier.put(f(successor), successor)
        else:
            continue

    return [None, 0]


# Implement dfs algorithm which translates the pesudocode from the lecture ppt
def dfs_alg(initialized_board):
    # follow the LIFO
    frontier = [initialized_board]
    explored = set()
    explored.add(convert_state(initialized_board))
    while len(frontier) > 0:
        curr = frontier.pop()
        successors_dfs = successors_state(curr)
        for successor_dfs in successors_dfs:
            if if_reach_goal(successor_dfs):
                return [successor_dfs, g(successor_dfs)]
            # check for pruning if not append into the expanded set
            if convert_state(successor_dfs) not in explored:
                explored.add(convert_state(successor_dfs))
                frontier.append(successor_dfs)
    return [None, 0]


# Implement dominated a star algorithm which translates the pesudocode from the lecture ppt
def dominated_a_star_alg(initialized_board):
    frontier = PriorityQ()
    frontier.put(f_dominant(initialized_board), initialized_board)
    explored = set()
    while not frontier.is_empty():
        curr = frontier.pop()[1]
        if convert_state(curr) not in explored:
            explored.add(convert_state(curr))
            successors = successors_state(curr)
            for successor in successors:
                if if_reach_goal(successor):
                    return [successor, f_dominant(successor)]
                else:
                    frontier.put(f_dominant(successor), successor)
        else:
            continue

    return [None, 0]


# write the output into output file
def result(algorithm, cost_of_step):
    file_input = ""
    for char in range(len(sys.argv[1]) - 4):
        file_input += sys.argv[1][char]
    output_file = f"{file_input}sol_{algorithm}.txt"
    output = open(output_file, "w")
    output.write(f"Cost of the solution: {cost_of_step[1]}\n")
    total_cost = cost_of_step[1]
    output_list = []
    if cost_of_step[0] is not None:
        while cost_of_step[0] is not None:
            output_list += [cost_of_step[0]]
            cost_of_step[0] = cost_of_step[0].last_board
    while total_cost >= 0:
        output.write(convert_state(output_list[total_cost]))
        total_cost -= 1
    output.close()


# main function to test
if __name__ == '__main__':
    read_state_board = read_inputfile()
    output1 = a_star_alg(read_state_board)
    output2 = dfs_alg(read_state_board)
    output3 = dominated_a_star_alg(read_state_board)
    result(algorithm="astar", cost_of_step=output1)
    result(algorithm="dfs", cost_of_step=output2)




