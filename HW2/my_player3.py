import numpy as np
import copy

INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'
BOARD_SIZE = 5
UNOCCUPIED = 0
BLACK = 1
WHITE = 2
# Right, Bottom, Left, Up
X_CHANGES = [1, 0, -1, 0]
Y_CHANGES = [0, 1, 0, -1]


class MyPlayer:
    def __init__(self, side, previous_game_state, current_game_state):
        self.side = side
        self.opponent_side = WHITE if self.side == BLACK else BLACK
        self.previous_game_state = previous_game_state
        self.current_game_state = current_game_state

    def find_valid_moves(self):
        valid_moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.current_game_state[i][j] == UNOCCUPIED:
                    if self.check_for_liberty(self.current_game_state, i, j, self.side):
                        # Check for 'KO' rule before validating this move!
                        if not self.check_for_ko(i, j):
                            valid_moves.append((i, j))
                    # Check if we are capturing some stones by doing this move
                    else:
                        for index in range(len(X_CHANGES)):
                            new_i = i + X_CHANGES[index]
                            new_j = j + Y_CHANGES[index]
                            if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                                if self.current_game_state[new_i][new_j] == self.opponent_side:
                                    # If there is a group of opponent_side that has no liberty with our move then we
                                    # can capture them and do this move!
                                    new_game_state = copy.deepcopy(self.current_game_state)
                                    new_game_state[i][j] = self.side
                                    if not self.check_for_liberty(new_game_state, new_i, new_j,
                                                                  self.opponent_side):
                                        # Check for 'KO' rule before validating this move!
                                        if not self.check_for_ko(i, j):
                                            valid_moves.append((i, j))
                                        break

                        # If the for loop did not break at all, then all of our neighbors have liberty and we cannot
                        # do this move

        return valid_moves

    def check_for_liberty(self, game_state, i, j, side):
        stack = [(i, j)]
        visited = set()
        while stack:
            top_node = stack.pop()
            visited.add(top_node)
            for index in range(len(X_CHANGES)):
                new_i = top_node[0] + X_CHANGES[index]
                new_j = top_node[1] + Y_CHANGES[index]
                if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                    if (new_i, new_j) in visited:
                        continue
                    elif game_state[new_i][new_j] == UNOCCUPIED:
                        return True
                    elif game_state[new_i][new_j] == side and (new_i, new_j) not in visited:
                        stack.append((new_i, new_j))
        return False

    def check_for_ko(self, i, j):
        if self.previous_game_state[i][j] != self.side:
            return False
        new_game_state = copy.deepcopy(self.current_game_state)
        new_game_state[i][j] = self.side
        opponent_i, opponent_j = self.opponent_move()
        for index in range(len(X_CHANGES)):
            new_i = i + X_CHANGES[index]
            new_j = j + Y_CHANGES[index]
            if new_i == opponent_i and new_j == opponent_j:
                # If opponent group does not have liberty then delete all of them
                if not self.check_for_liberty(new_game_state, new_i, new_j, self.opponent_side):
                    # Delete all of the group from the board and check if we have the same exact board as before
                    self.delete_group(new_game_state, new_i, new_j, self.opponent_side)
        # If opponent's move is not out neighbor then it cannot be KO!
        return np.array_equal(new_game_state, self.previous_game_state)

    def opponent_move(self):
        if np.array_equal(self.current_game_state, self.previous_game_state):
            return None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.current_game_state[i][j] != self.previous_game_state[i][j]\
                        and self.current_game_state[i][j] != UNOCCUPIED:
                    # Just a double check that the difference is a stone that belongs to the opponent!
                    # TODO delete this
                    assert self.current_game_state[i][j] == self.opponent_side, "Houston we've got a problem!"
                    return i, j

    def delete_group(self, game_state, i, j, side):
        stack = [(i, j)]
        visited = set()
        while stack:
            top_node = stack.pop()
            visited.add(top_node)
            game_state[top_node[0]][top_node[1]] = UNOCCUPIED
            for index in range(len(X_CHANGES)):
                new_i = top_node[0] + X_CHANGES[index]
                new_j = top_node[1] + Y_CHANGES[index]
                if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                    if (new_i, new_j) in visited:
                        continue
                    elif game_state[new_i][new_j] == side:
                        stack.append((new_i, new_j))
        return game_state


def read_input(input_file_name = INPUT_FILE_NAME):
    with open(input_file_name) as input_file:
        input_file_lines = [input_file_line.strip() for input_file_line in input_file.readlines()]
        # side = 1 => we are black, side = 2 => we are white
        side = int(input_file_lines[0])
        previous_game_state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        current_game_state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(1, 6):
            for j in range(len(input_file_lines[i])):
                previous_game_state[i - 1][j] = input_file_lines[i][j]
        for i in range(6, 11):
            for j in range(len(input_file_lines[i])):
                current_game_state[i - 6][j] = input_file_lines[i][j]
        return side, previous_game_state, current_game_state


def write_output():
    with open(OUTPUT_FILE_NAME, 'w') as output_file:
        output_file.write('2,3')


if __name__ == '__main__':
    side, previous_game_state, current_game_state = read_input()
    my_player = MyPlayer(side, previous_game_state, current_game_state)
    print(my_player.find_valid_moves())
    # write_output()
