import unittest
from tic_tac_toe import *


class TestBoard(unittest.TestCase):

    def test_empty_board_3(self):
        self.assertEqual(empty_board(3), [['.', '.', '.'], ['.', '.'], ['.']])

    def test_empty_board_5(self):
        self.assertEqual(empty_board(5),
                         [['.', '.', '.', '.', '.'], ['.', '.', '.', '.'],
                          ['.', '.', '.'], ['.', '.'], ['.']])

    def test_make_move(self):
        board = empty_board(5)
        make_move(board, (1, 1), 'x')
        self.assertEqual(board,
                         [['.', '.', '.', '.', '.'], ['.', 'x', '.', '.'],
                          ['.', '.', '.'], ['.', '.'], ['.']])
        make_move(board, (1, 2), 'x')
        make_move(board, (1, 3), 'x')
        make_move(board, (2, 2), 'x')
        make_move(board, (3, 1), 'x')
        self.assertEqual(board,
                         [['.', '.', '.', '.', '.'], ['.', 'x', 'x', 'x'],
                          ['.', '.', 'x'], ['.', 'x'], ['.']])
        make_move(board, (0, 0), 'o')
        make_move(board, (0, 1), 'o')
        make_move(board, (0, 2), 'o')
        make_move(board, (0, 3), 'o')
        make_move(board, (0, 4), 'o')
        self.assertEqual(board,
                         [['o', 'o', 'o', 'o', 'o'], ['.', 'x', 'x', 'x'],
                          ['.', '.', 'x'], ['.', 'x'], ['.']])

    def test_make_move_undo(self):
        # undo move
        board = [['o', '.', '.'], ['.', '.'], ['x']]
        make_move(board, (0, 0), '.')
        self.assertEqual(board, [['.', '.', '.'], ['.', '.'], ['x']])

    def test_winner(self):
        board = [['.', '.', '.', '.', '.'], ['.', 'x', 'x', 'x'],
                 ['.', '.', 'x'], ['.', 'x'], ['.']]
        self.assertEqual(winner(board, 2), 'x')
        self.assertEqual(winner(board, 3), 'x')
        self.assertIsNone(winner(board, 4), None)
        board = [['o', 'o', 'o', 'o', 'o'], ['.', 'x', 'x', 'x'],
                 ['.', '.', 'x'], ['.', 'x'], ['.']]
        self.assertEqual(winner(board, 5), 'o')
        self.assertIsNone(winner(board, 6), None)

    def test_winner_draw(self):
        board = [['o', 'o', 'x'], ['x', 'x'], ['o']]
        self.assertEqual(winner(board, 3), '.')

    def test_is_draw(self):
        # is empty board already a draw:
        self.assertFalse(is_draw(empty_board(3), 3))
        # need more symbols than board size:
        self.assertTrue(is_draw(empty_board(3), 4))
        board = [['o', '.', 'x'], ['x', 'x'], ['o']]
        self.assertTrue(is_draw(board, 3))
        self.assertFalse(is_draw(board, 2))
        board[0][2] = '.'
        self.assertFalse(is_draw(board, 3))


class TestAI(unittest.TestCase):
    # Can be time consuming due to lime limits of negamax

    def test_heuristics(self):
        board = empty_board(5)
        board[0][0] = 'o'
        self.assertEqual(heuristics(board, 3, 'o'), 3)
        self.assertEqual(heuristics(board, 3, 'x'), -3)
        board[1][0] = 'o'
        self.assertEqual(heuristics(board, 3, 'o'), 6)
        self.assertEqual(heuristics(board, 3, 'x'), -6)
        board[0][4] = 'x'
        self.assertEqual(heuristics(board, 3, 'o'), 4)
        board[2][0] = 'x'
        self.assertEqual(heuristics(board, 3, 'o'), -2)
        self.assertEqual(heuristics(board, 3, 'x'), 2)
        self.assertEqual(heuristics(board, 2, 'o'), math.inf)
        self.assertEqual(heuristics(board, 2, 'x'), -math.inf)

    def test_negamax_move(self):
        # This test can take a few seconds due to negamax time limit
        # Block opponent's winning move:
        board = [['.', '.', 'o'], ['x', 'o'], ['.']]
        self.assertEqual(negamax_move(board, 3, 'x'), (2, 0))
        board[0][0] = 'x'
        # Play winning moves:
        self.assertEqual(negamax_move(board, 3, 'x'), (2, 0))
        self.assertEqual(negamax_move(board, 3, 'o'), (2, 0))
        # Block opponent's winning move:
        board = [['.', 'x', 'o', '.', '.', '.'], ['.', 'x', 'x', 'o', '.'],
                 ['.', 'x', 'x', 'o'], ['o', '.', 'o'], ['.', '.'], ['.']]
        self.assertEqual(negamax_move(board, 4, 'o', 1), (3, 1))
        self.assertEqual(negamax_move(board, 4, 'o', 5), (3, 1))
