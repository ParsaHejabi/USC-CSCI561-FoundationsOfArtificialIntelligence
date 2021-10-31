import copy

import numpy as np

INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'
BOARD_SIZE = 5
UNOCCUPIED = 0
BLACK = 1
WHITE = 2
KOMI = 3
# Right, Bottom, Left, Up
X_CHANGES = [1, 0, -1, 0]
Y_CHANGES = [0, 1, 0, -1]


class MyPlayer:
    def __init__(self, side, previous_game_state, current_game_state):
        self.side = side
        self.opponent_side = self.get_opponent_side(self.side)
        self.previous_game_state = previous_game_state
        self.current_game_state = current_game_state

    def alpha_beta_search(self, search_depth, branching_factor):
        max_move, max_move_value = self.max_value(self.current_game_state, self.side, search_depth, 0, branching_factor,
                                                  -np.inf, np.inf, None)
        # DEBUG
        # print(max_move, max_move_value)
        write_output(max_move)

    def max_value(self, game_state, side, search_depth, current_depth, branching_factor, alpha, beta, last_move):
        if search_depth == current_depth:
            return self.evaluate_game_state(game_state, side)
        max_move_value = -np.inf
        max_move = None
        valid_moves = self.find_valid_moves(game_state, side)
        if last_move != (-1, -1):
            valid_moves.append((-1, -1))
        for valid_move in valid_moves[:branching_factor]:
            # Create new game state
            opponent_side = self.get_opponent_side(side)
            if valid_move == (-1, -1):
                new_game_state = copy.deepcopy(game_state)
            else:
                new_game_state = self.move(game_state, side, valid_move)
            min_move_value = self.min_value(new_game_state, opponent_side, search_depth, current_depth + 1,
                                            branching_factor, alpha, beta, valid_move)
            if max_move_value < min_move_value:
                max_move_value = min_move_value
                max_move = valid_move
            if max_move_value >= beta:
                if current_depth == 0:
                    return max_move, max_move_value
                else:
                    return max_move_value
            alpha = max(alpha, max_move_value)
        if current_depth == 0:
            return max_move, max_move_value
        else:
            return max_move_value

    def min_value(self, game_state, side, search_depth, current_depth, branching_factor, alpha, beta, last_move):
        if search_depth == current_depth:
            return self.evaluate_game_state(game_state, side)
        min_move_value = np.inf
        valid_moves = self.find_valid_moves(game_state, side)
        if last_move != (-1, -1):
            valid_moves.append((-1, -1))
        for valid_move in valid_moves[:branching_factor]:
            # Create new game state
            opponent_side = self.get_opponent_side(side)
            if valid_move == (-1, -1):
                new_game_state = copy.deepcopy(game_state)
            else:
                new_game_state = self.move(game_state, side, valid_move)
            max_move_value = self.max_value(new_game_state, opponent_side, search_depth, current_depth + 1,
                                            branching_factor, alpha, beta, valid_move)
            if max_move_value < min_move_value:
                min_move_value = max_move_value
            if min_move_value <= alpha:
                return min_move_value
            beta = min(beta, min_move_value)
        return min_move_value

    def evaluate_game_state(self, game_state, side):
        # Define heuristic here
        # Count number of sides stones - opponent stones
        opponent_side = self.get_opponent_side(side)
        side_count = 0
        side_liberty = set()
        opponent_count = 0
        opponent_liberty = set()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if game_state[i][j] == side:
                    side_count += 1
                elif game_state[i][j] == opponent_side:
                    opponent_count += 1
                # This point should be UNOCCUPIED!
                else:
                    for index in range(len(X_CHANGES)):
                        new_i = i + X_CHANGES[index]
                        new_j = j + Y_CHANGES[index]
                        if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                            if game_state[new_i][new_j] == side:
                                side_liberty.add((new_i, new_j))
                            elif game_state[new_i][new_j] == opponent_side:
                                opponent_liberty.add((new_i, new_j))

        side_edge_count = 0
        opponent_side_edge_count = 0
        for j in range(BOARD_SIZE):
            if game_state[0][j] == side or game_state[BOARD_SIZE - 1][j] == side:
                side_edge_count += 1
            if game_state[j][0] == side or game_state[j][BOARD_SIZE - 1] == side:
                side_edge_count += 1
            if game_state[0][j] == opponent_side or game_state[BOARD_SIZE - 1][j] == opponent_side:
                opponent_side_edge_count += 1
            if game_state[j][0] == opponent_side or game_state[j][BOARD_SIZE - 1] == opponent_side:
                opponent_side_edge_count += 1

        score = min(max((len(side_liberty) - len(opponent_liberty)), -4), 4) + (
                -4 * self.calculate_euler_number(game_state, side)) + (
                            5 * (side_count - opponent_count)) - side_edge_count
        if self.side == WHITE:
            score += 2 * KOMI
        return score

    def move(self, game_state, side, move):
        new_game_state = copy.deepcopy(game_state)
        # We know that the move which is going to be done is definitely valid for this side!
        # We checked for liberty and KO before! So we can do the move!
        new_game_state[move[0]][move[1]] = side
        # Now we check if we have to delete opponents group or not
        for index in range(len(X_CHANGES)):
            new_i = move[0] + X_CHANGES[index]
            new_j = move[1] + Y_CHANGES[index]
            if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                opponent_side = self.get_opponent_side(side)
                if new_game_state[new_i][new_j] == opponent_side:
                    # DFS!
                    stack = [(new_i, new_j)]
                    visited = set()
                    opponent_group_should_be_deleted = True
                    while stack:
                        top_node = stack.pop()
                        visited.add(top_node)
                        for index in range(len(X_CHANGES)):
                            new_new_i = top_node[0] + X_CHANGES[index]
                            new_new_j = top_node[1] + Y_CHANGES[index]
                            if 0 <= new_new_i < BOARD_SIZE and 0 <= new_new_j < BOARD_SIZE:
                                if (new_new_i, new_new_j) in visited:
                                    continue
                                elif new_game_state[new_new_i][new_new_j] == UNOCCUPIED:
                                    opponent_group_should_be_deleted = False
                                    break
                                elif new_game_state[new_new_i][new_new_j] == opponent_side and \
                                        (new_new_i, new_new_j) not in visited:
                                    stack.append((new_new_i, new_new_j))

                    if opponent_group_should_be_deleted:
                        for stone in visited:
                            new_game_state[stone[0]][stone[1]] = UNOCCUPIED
        return new_game_state

    def calculate_euler_number(self, game_state, side):
        opponent_side = self.get_opponent_side(side)
        new_game_state = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        # First copy the original game_state
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                new_game_state[i + 1][j + 1] = game_state[i][j]

        q1_side = 0
        q2_side = 0
        q3_side = 0
        q1_opponent_side = 0
        q2_opponent_side = 0
        q3_opponent_side = 0

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                new_game_sub_state = new_game_state[i: i + 2, j: j + 2]
                q1_side += self.count_q1(new_game_sub_state, side)
                q2_side += self.count_q2(new_game_sub_state, side)
                q3_side += self.count_q3(new_game_sub_state, side)
                q1_opponent_side += self.count_q1(new_game_sub_state, opponent_side)
                q2_opponent_side += self.count_q2(new_game_sub_state, opponent_side)
                q3_opponent_side += self.count_q3(new_game_sub_state, opponent_side)

        return (q1_side - q3_side + 2 * q2_side - (q1_opponent_side - q3_opponent_side + 2 * q2_opponent_side)) / 4

    def count_q1(self, game_sub_state, side):
        if ((game_sub_state[0][0] == side and game_sub_state[0][1] != side
             and game_sub_state[1][0] != side and game_sub_state[1][1] != side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] == side
                    and game_sub_state[1][0] != side and game_sub_state[1][1] != side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] != side
                    and game_sub_state[1][0] == side and game_sub_state[1][1] != side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] != side
                    and game_sub_state[1][0] != side and game_sub_state[1][1] == side)):
            return 1
        else:
            return 0

    def count_q2(self, game_sub_state, side):
        if ((game_sub_state[0][0] == side and game_sub_state[0][1] != side
             and game_sub_state[1][0] != side and game_sub_state[1][1] == side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] == side
                    and game_sub_state[1][0] == side and game_sub_state[1][1] != side)):
            return 1
        else:
            return 0

    def count_q3(self, game_sub_state, side):
        if ((game_sub_state[0][0] == side and game_sub_state[0][1] == side
             and game_sub_state[1][0] == side and game_sub_state[1][1] != side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] == side
                    and game_sub_state[1][0] == side and game_sub_state[1][1] == side)
                or (game_sub_state[0][0] == side and game_sub_state[0][1] != side
                    and game_sub_state[1][0] == side and game_sub_state[1][1] == side)
                or (game_sub_state[0][0] != side and game_sub_state[0][1] == side
                    and game_sub_state[1][0] == side and game_sub_state[1][1] == side)):
            return 1
        else:
            return 0

    def find_valid_moves(self, game_state, side):
        valid_moves = {'3side': [], '1capturing': [], '2regular': []}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if game_state[i][j] == UNOCCUPIED:
                    if self.check_for_liberty(game_state, i, j, side):
                        # Check for 'KO' rule before validating this move!
                        if not self.check_for_ko(i, j):
                            if i == 0 or j == 0 or i == BOARD_SIZE - 1 or j == BOARD_SIZE - 1:
                                valid_moves.get('3side').append((i, j))
                            else:
                                valid_moves.get('2regular').append((i, j))
                    # Check if we are capturing some stones by doing this move
                    else:
                        for index in range(len(X_CHANGES)):
                            new_i = i + X_CHANGES[index]
                            new_j = j + Y_CHANGES[index]
                            if 0 <= new_i < BOARD_SIZE and 0 <= new_j < BOARD_SIZE:
                                opponent_side = self.get_opponent_side(side)
                                if game_state[new_i][new_j] == opponent_side:
                                    # If there is a group of opponent_side that has no liberty with our move then we
                                    # can capture them and do this move!
                                    new_game_state = copy.deepcopy(game_state)
                                    new_game_state[i][j] = side
                                    if not self.check_for_liberty(new_game_state, new_i, new_j,
                                                                  opponent_side):
                                        # Check for 'KO' rule before validating this move!
                                        if not self.check_for_ko(i, j):
                                            valid_moves.get('1capturing').append((i, j))
                                        break

                        # If the for loop did not break at all, then all of our neighbors have liberty and we cannot
                        # do this move

        valid_moves_list = []
        for valid_move in valid_moves.get('1capturing'):
            valid_moves_list.append(valid_move)
        for valid_move in valid_moves.get('2regular'):
            valid_moves_list.append(valid_move)
        for valid_move in valid_moves.get('3side'):
            valid_moves_list.append(valid_move)

        # DEBUG
        # print(valid_moves_list)
        return valid_moves_list

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

    def get_opponent_side(self, side):
        return WHITE if side == BLACK else BLACK

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
                if self.current_game_state[i][j] != self.previous_game_state[i][j] \
                        and self.current_game_state[i][j] != UNOCCUPIED:
                    # Just a double check that the difference is a stone that belongs to the opponent!
                    # assert self.current_game_state[i][j] == self.opponent_side, "Houston we've got a problem!"
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


def read_input(input_file_name=INPUT_FILE_NAME):
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


def write_output(next_move):
    with open(OUTPUT_FILE_NAME, 'w') as output_file:
        if next_move is None or next_move == (-1, -1):
            output_file.write('PASS')
        else:
            output_file.write(f'{next_move[0]},{next_move[1]}')


if __name__ == '__main__':
    side, previous_game_state, current_game_state = read_input()
    my_player = MyPlayer(side, previous_game_state, current_game_state)
    my_player.alpha_beta_search(6, 20)
