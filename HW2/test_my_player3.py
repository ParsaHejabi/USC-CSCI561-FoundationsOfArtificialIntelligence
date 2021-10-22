import unittest
from my_player3 import MyPlayer
from my_player3 import read_input
import numpy as np

BOARD_SIZE = 5
UNOCCUPIED = 0
BLACK = 1
WHITE = 2


class TestMyPlayer(unittest.TestCase):
    def test_opponent_move(self):
        side, previous_game_state, current_game_state = read_input('tests/test_opponent_move1.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertIsNone(my_player.opponent_move())
        side, previous_game_state, current_game_state = read_input('tests/test_opponent_move2.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        with self.assertRaises(AssertionError):
            my_player.opponent_move()
        side, previous_game_state, current_game_state = read_input('tests/test_opponent_move3.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertEqual(my_player.opponent_move(), (2, 2))
        side, previous_game_state, current_game_state = read_input('tests/test_opponent_move4.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertEqual(my_player.opponent_move(), (3, 2))
        side, previous_game_state, current_game_state = read_input('tests/test_opponent_move5.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertEqual(my_player.opponent_move(), (3, 2))

    def test_check_for_liberty(self):
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_liberty1.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertFalse(my_player.check_for_liberty(my_player.current_game_state, 0, 0, BLACK))
        self.assertFalse(my_player.check_for_liberty(my_player.current_game_state, 0, 2, WHITE))
        self.assertTrue(my_player.check_for_liberty(my_player.current_game_state, 0, 3, BLACK))
        self.assertFalse(my_player.check_for_liberty(my_player.current_game_state, 0, 4, BLACK))
        self.assertTrue(my_player.check_for_liberty(my_player.current_game_state, 1, 4, WHITE))
        self.assertTrue(my_player.check_for_liberty(my_player.current_game_state, 1, 3, BLACK))
        self.assertTrue(my_player.check_for_liberty(my_player.current_game_state, 2, 2, BLACK))
        self.assertFalse(my_player.check_for_liberty(my_player.current_game_state, 4, 0, WHITE))

    def test_delete_group(self):
        side, previous_game_state, current_game_state = read_input('tests/test_delete_group1.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(my_player.delete_group(my_player.current_game_state, 2, 2,
                                                              my_player.current_game_state[2][2]),
                                       np.array([[1, 1, 2, 1, 0],
                                                 [1, 2, 2, 1, 2],
                                                 [2, 2, 0, 2, 1],
                                                 [0, 0, 0, 2, 1],
                                                 [0, 2, 2, 1, 2]])))
        self.assertTrue(np.array_equal(my_player.delete_group(my_player.current_game_state, 4, 0,
                                                              WHITE),
                                       np.array([[1, 1, 2, 1, 0],
                                                 [1, 2, 2, 1, 2],
                                                 [2, 2, 0, 2, 1],
                                                 [0, 0, 0, 2, 1],
                                                 [0, 0, 0, 1, 2]])))

    def test_check_for_ko(self):
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko1.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertFalse(my_player.check_for_ko(2, 3))
        self.assertFalse(my_player.check_for_ko(3, 3))
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko2.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(my_player.check_for_ko(2, 3))
        self.assertFalse(my_player.check_for_ko(0, 0))
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko3.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(my_player.check_for_ko(4, 3))
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko3.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(my_player.check_for_ko(4, 3))
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko4.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(my_player.check_for_ko(3, 4))
        side, previous_game_state, current_game_state = read_input('tests/test_check_for_ko5.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(my_player.check_for_ko(4, 1))

    def test_find_valid_moves(self):
        side, previous_game_state, current_game_state = read_input('tests/test_find_valid_moves1.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(np.array(my_player.find_valid_moves()).sort(), np.array([(0, 0), (0, 1), (0, 2),
                                                                                                (0, 3), (0, 4), (1, 0),
                                                                                                (1, 1), (1, 3), (1, 4),
                                                                                                (2, 0), (2, 4), (3, 0),
                                                                                                (3, 1), (3, 3), (3, 4),
                                                                                                (4, 0), (4, 1), (4, 2),
                                                                                                (4, 3), (4, 4)]).sort()
                                       )
                        )

        side, previous_game_state, current_game_state = read_input('tests/test_find_valid_moves2.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(np.array(my_player.find_valid_moves()).sort(), np.array([(0, 0), (0, 1), (0, 2),
                                                                                                (0, 4), (2, 0), (2, 4),
                                                                                                (3, 3), (3, 4), (4, 0),
                                                                                                (4, 1), (4, 2), (4, 3),
                                                                                                (4, 4)]).sort()
                                       )
                        )

        side, previous_game_state, current_game_state = read_input('tests/test_find_valid_moves3.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(np.array(my_player.find_valid_moves()).sort(), np.array([(0, 3), (0, 4), (1, 2),
                                                                                                (1, 3), (1, 4), (2, 1),
                                                                                                (2, 2), (2, 3), (2, 4),
                                                                                                (3, 0), (3, 1), (3, 2),
                                                                                                (3, 3), (3, 4), (4, 0),
                                                                                                (4, 1), (4, 2), (4, 3),
                                                                                                (4, 4)]).sort()
                                       )
                        )

        side, previous_game_state, current_game_state = read_input('tests/test_find_valid_moves4.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(np.array(my_player.find_valid_moves()).sort(), np.array([]).sort()))

        side, previous_game_state, current_game_state = read_input('tests/test_find_valid_moves5.txt')
        my_player = MyPlayer(side, previous_game_state, current_game_state)
        self.assertTrue(np.array_equal(np.array(my_player.find_valid_moves()).sort(), np.array([(0, 3)]).sort()))
