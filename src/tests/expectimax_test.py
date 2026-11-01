import unittest

from bitboard import Bitboard
from expectimax import Expectimax
from heuristics import Heuristics


class HeuristicsForTest(Heuristics):
    WIN_SCORE = 2 * 4 ** 15

    def evaluate(self, board: Bitboard) -> float:
        if any(board.get_cell(index) == 7 for index in range(16)):
            return self.WIN_SCORE
        return 0.0


class TestExpectimax(unittest.TestCase):
    @staticmethod
    def create_one_way_test_board() -> Bitboard:
        board = Bitboard()
        for index, value in (
                (1, 1),
                (4, 4),
                (5, 2),
                (7, 3),
                (8, 2),
                (11, 6),
                (12, 1),
                (13, 6),
                (14, 1)):
            board = board.set_cell(index, value)
        return board

    @staticmethod
    def create_two_way_test_board() -> Bitboard:
        board = Bitboard()
        for index, value in (
                (0, 1),
                (2, 1),
                (4, 5),
                (6, 6),
                (8, 1),
                (9, 6),
                (11, 5)):
            board = board.set_cell(index, value)
        return board

    @staticmethod
    def has_adjacent_64s(board: Bitboard) -> bool:
        positions = [
            index for index in range(16) if board.get_cell(index) == 6
        ]
        first, second = positions
        return (
            abs(first // 4 - second // 4)
            + abs(first % 4 - second % 4) == 1
        )

    def test_win_heuristic_score_exceeds_normal_scores(self):
        heuristics = HeuristicsForTest()
        board = self.create_one_way_test_board()
        winning_board = board.set_cell(0, 7)

        self.assertEqual(heuristics.evaluate(winning_board),
                         HeuristicsForTest.WIN_SCORE)
        self.assertEqual(heuristics.evaluate(board), 0.0)
        self.assertGreater(HeuristicsForTest.WIN_SCORE, 4 ** 15)
        self.assertGreater(HeuristicsForTest.WIN_SCORE, 2 ** 16 * 64)

    def test_get_best_move_selects_the_only_winning_move(self):
        board = self.create_one_way_test_board()
        heuristics = HeuristicsForTest()
        ai = Expectimax(min_depth=2, max_depth=2, heuristics=heuristics)

        self.assertEqual(ai.get_best_move(board), "left")

    def test_exactly_two_moves_create_adjacent_64s(self):
        board = self.create_two_way_test_board()
        adjacent_moves = [
            direction for direction in ("left", "right", "up", "down")
            if self.has_adjacent_64s(board.move(direction))
        ]

        self.assertEqual(adjacent_moves, ["left", "down"])
