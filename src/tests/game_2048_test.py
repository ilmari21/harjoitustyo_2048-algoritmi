import unittest

from game_2048 import Game2048


class TestGame2048(unittest.TestCase):
    def test_initial_board(self):
        game = Game2048()
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.board.get_empty_cells()), 14)

    def test_reset(self):
        game = Game2048()
        game.move("up")
        game.reset()
        self.assertEqual(game.score, 0)
        self.assertEqual(len(game.board.get_empty_cells()), 14)
