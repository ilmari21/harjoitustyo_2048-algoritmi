import unittest
from unittest.mock import Mock

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

    def test_get_search_depth_increases_as_empty_cells_decrease(self):
        ai = Expectimax(min_depth=2, max_depth=6)

        for empty_cells, expected_depth in (
                (11, 3),
                (7, 4),
                (3, 5),
                (2, 6)):
            board = Bitboard()
            for index in range(16 - empty_cells):
                board = board.set_cell(index, 1)

            self.assertEqual(ai.get_search_depth(board), expected_depth)

    def test_invalid_search_depths_raise_value_error(self):
        for min_depth, max_depth in (
                (1, 2),
                (2, 1),
                (2, 7),
                (7, 7)):
            with self.subTest(min_depth=min_depth, max_depth=max_depth):
                with self.assertRaises(ValueError):
                    Expectimax(min_depth, max_depth)

    def test_expectimax_uses_search_depth_when_depth_is_not_given(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(min_depth=2, max_depth=2, heuristics=heuristics)
        ai.get_search_depth = Mock(return_value=0)
        board = Bitboard()

        self.assertEqual(ai.expectimax(board), 42.0)
        ai.get_search_depth.assert_called_once_with(board)
        heuristics.evaluate.assert_called_once_with(board)

    def test_expectimax_evaluates_board_when_depth_is_zero(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(min_depth=2, max_depth=2, heuristics=heuristics)
        board = Bitboard().set_cell(0, 1)

        self.assertEqual(ai.expectimax(board, depth=0), 42.0)
        heuristics.evaluate.assert_called_once_with(board)

    def test_expectimax_returns_cached_score(self):
        ai = Expectimax(min_depth=2, max_depth=2)
        board = Bitboard().set_cell(0, 1)
        ai.transposition_table[("max", board.return_board(), 2)] = 123.0

        self.assertEqual(ai.expectimax(board, depth=2), 123.0)

    def test_expectimax_evaluates_board_without_valid_moves(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(min_depth=2, max_depth=2, heuristics=heuristics)
        board = Bitboard()
        for index in range(16):
            row, column = divmod(index, 4)
            value = 1 if (row + column) % 2 == 0 else 2
            board = board.set_cell(index, value)

        self.assertEqual(ai.expectimax(board, depth=2), 42.0)
        heuristics.evaluate.assert_called_once_with(board)

    def test_expectimax_evaluates_moved_board_at_depth_one(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        board = self.create_one_way_test_board()
        ai = Expectimax(2, 2, heuristics=heuristics)
        valid_moves = ai.get_valid_moves(board)

        self.assertEqual(
            ai.expectimax(board, depth=1),
            42.0,
        )
        self.assertEqual(heuristics.evaluate.call_count, len(valid_moves))

    def test_expectimax_uses_chance_nodes_at_depth_greater_than_one(self):
        board = self.create_one_way_test_board()
        ai = Expectimax(2, 2)
        ai.expectimax_chance_node = Mock(return_value=42.0)
        valid_moves = ai.get_valid_moves(board)

        self.assertEqual(
            ai.expectimax(board, depth=2),
            42.0,
        )
        self.assertEqual(
            ai.expectimax_chance_node.call_count,
            len(valid_moves),
        )

    def test_chance_node_evaluates_board_when_depth_is_zero(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(2, 2, heuristics=heuristics)
        board = Bitboard().set_cell(0, 1)

        self.assertEqual(ai.expectimax_chance_node(board, depth=0), 42.0)
        heuristics.evaluate.assert_called_once_with(board)

    def test_chance_node_returns_cached_score(self):
        ai = Expectimax(2, 2)
        board = Bitboard().set_cell(0, 1)
        ai.transposition_table[("chance", board.return_board(), 2)] = 123.0

        self.assertEqual(ai.expectimax_chance_node(board, depth=2), 123.0)

    def test_chance_node_evaluates_game_over_board(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(2, 2, heuristics=heuristics)
        board = Bitboard()
        for index in range(16):
            row, column = divmod(index, 4)
            value = 1 if (row + column) % 2 == 0 else 2
            board = board.set_cell(index, value)

        self.assertEqual(ai.expectimax_chance_node(board, depth=2), 42.0)
        heuristics.evaluate.assert_called_once_with(board)

    def test_chance_node_evaluates_full_board_without_moves(self):
        heuristics = Mock()
        heuristics.evaluate.return_value = 42.0
        ai = Expectimax(2, 2, heuristics=heuristics)
        board = Bitboard()
        for index in range(16):
            board = board.set_cell(index, 1)

        self.assertEqual(ai.expectimax_chance_node(board, depth=2), 42.0)
        heuristics.evaluate.assert_called_once_with(board)
