import numpy as np

BOARD_SIZE = 3

ONGOING = -1
DRAW = 0
X_WIN = 1
O_WIN = 2


class Board:

    def __init__(self, state=None, show_board=False, show_result=False):
        """ board cell:
                Empty -> 0
                X -> 1
                O -> 2
        """
        if state is None:
            self.state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int)
        else:
            self.state = state.copy()
        self.game_result = ONGOING
        self.show_board  = show_board
        self.show_result = show_result

    def set_show_board(self, show_board):
        self.show_board = show_board

    def encode_state(self):
        """ Encode the current state of the board as a string
        """
        return ''.join([str(self.state[i][j]) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])

    def reset(self):
        self.state.fill(0)
        self.game_result = ONGOING

    def is_valid_move(self, row, col):
        return row < BOARD_SIZE and row >= 0 and col < BOARD_SIZE and col >=0 and self.state[row][col] == 0

    def move(self, row, col, player):
        """
        Parameters
        ----------
        row : 0, 1, 2
        col : 0, 1, 2
        player: X -> 1, O -> 2

        Returns
        -------
        state: state after the move
        result: game result after the move
        """
        if not self.is_valid_move(row, col):
            print (row, col)
            self.print_board()
            raise ValueError("Invalid Move")

        self.state[row][col] = player
        self.game_result = self._check_winner()

        if self.show_board:
            p = 'X' if player == 1 else 'O'
            print('player {} moved: {}, {}'.format(p, row, col))
            self.print_board()

        if self.show_result:
            self.game_result_report()

        return self.state, self.game_result

    def game_over(self):
        return self.game_result != ONGOING


    def print_board(self):
        board = self.encode_state()
        board = board.replace('0', ' ')
        board = board.replace('1', 'X')
        board = board.replace('2', 'O')
        print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
        print('--- --- ---')
        print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
        print('--- --- ---')
        print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
        print()

    def game_result_report(self):
        if self.game_result is ONGOING:
            return
        print ('=' * 30)
        if self.game_result is DRAW:
            print ('Game Over : Draw'.center(30))
        elif self.game_result is X_WIN:
            print ('Game Over : Winner X'.center(30))
        elif self.game_result is O_WIN:
            print ('Game Over : Winner O'.center(30))
        print ('=' * 30)

    def _check_winner(self):
        # check each row and column
        for i in range(0, 3):
            if self.state[i][0] > 0 and self.state[i][0] == self.state[i][1] and self.state[i][1] == self.state[i][2]:
                return X_WIN if self.state[i][0] == 1 else O_WIN
            if self.state[0][i] > 0 and self.state[0][i] == self.state[1][i] and self.state[1][i] == self.state[2][i]:
                return X_WIN if self.state[0][i] == 1 else O_WIN

        # check diagonal
        if self.state[1][1] > 0 and self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]:
            return X_WIN if self.state[1][1] == 1 else O_WIN
        if self.state[1][1] > 0 and self.state[2][0] == self.state[1][1] and self.state[1][1] == self.state[0][2]:
            return X_WIN if self.state[1][1] == 1 else O_WIN

        # draw
        if (self.state == 0).sum() == 0:
            return DRAW

        return ONGOING


if __name__ == "__main__":
    board = Board()
    board.move(0, 0, 1)
    board.move(0, 1, 1)
    board.move(2, 2, 2)
    board.move(2, 1, 2)
    print()
    print(board.state)
    print()
    board.print_board()

