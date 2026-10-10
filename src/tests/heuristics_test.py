import unittest

from bitboard import Bitboard
from heuristics import Heuristics


class TestHeuristics(unittest.TestCase):
    def test_evaluate_matches_empty_cell_and_snake_scores(self):
        board = Bitboard()
        for index, value in ((0, 3), (5, 2), (15, 1)):
            board = board.set_cell(index, value)

        expected_empty_score = 13 * Heuristics.EMPTY_CELL_WEIGHT
        expected_snake_score = sum(
            board.get_cell(index) * weight
            for index, weight in enumerate(Heuristics.SNAKE_WEIGHTS)
        )

        self.assertEqual(
            Heuristics().evaluate(board),
            expected_empty_score + expected_snake_score,
        )

    def test_evaluate_empty_and_full_boards(self):
        heuristics = Heuristics()
        self.assertEqual(heuristics.evaluate(Bitboard()),
                         16 * Heuristics.EMPTY_CELL_WEIGHT)

        full_board = Bitboard()
        for index in range(16):
            full_board = full_board.set_cell(index, 1)

        self.assertEqual(
            heuristics.evaluate(full_board),
            sum(Heuristics.SNAKE_WEIGHTS),
        )
