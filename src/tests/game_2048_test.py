import random
import unittest

from bitboard import Bitboard
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

    def test_move_merges_tiles_and_updates_score(self):
        game = Game2048(random.Random(0))
        game.board = Bitboard().set_cell(0, 1).set_cell(1, 1)

        self.assertTrue(game.move("left"))

        self.assertEqual(game.score, 4)
        self.assertEqual(game.board.get_cell(0), 2)
        self.assertEqual(len(game.board.get_empty_cells()), 14)

    def test_spawn_random_tile_returns_false_when_board_is_full(self):
        game = Game2048()
        full_board = Bitboard()
        for index in range(16):
            full_board = full_board.set_cell(index, 1)
        game.board = full_board

        board_before_spawn = game.get_board()

        self.assertFalse(game.spawn_random_tile())
        self.assertEqual(game.get_board(), board_before_spawn)

    def test_spawn_random_tile_places_a_tile_on_an_empty_board(self):
        game = Game2048(random.Random(0))
        game.board = Bitboard()

        self.assertTrue(game.spawn_random_tile())

        self.assertEqual(len(game.board.get_empty_cells()), 15)
        spawned_tiles = [
            game.board.get_cell(index)
            for index in range(16)
            if game.board.get_cell(index) != 0
        ]
        self.assertEqual(len(spawned_tiles), 1)
        self.assertIn(spawned_tiles[0], (1, 2))

    def test_move_returns_false_when_board_does_not_change(self):
        game = Game2048()
        game.board = Bitboard().set_cell(0, 1)
        board_before_move = game.get_board()

        self.assertFalse(game.move("up"))
        self.assertEqual(game.get_board(), board_before_move)

    def test_tile_score(self):
        board = Bitboard()
        board = board.set_cell(0, 1)
        board = board.set_cell(1, 2)
        board = board.set_cell(2, 3)
        board = board.set_cell(3, 4)

        self.assertEqual(Game2048._tile_score(board), 4 + 16 + 48)
