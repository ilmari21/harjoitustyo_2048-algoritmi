import unittest

from bitboard import Bitboard


class TestBitboard(unittest.TestCase):
    def test_set_and_get_cell(self):
        board = Bitboard()
        board = board.set_cell(0, 1)
        self.assertEqual(board.get_cell(0), 1)
        self.assertEqual(board.get_cell(1), 0)

    def test_get_bit(self):
        board = Bitboard()
        board = board.set_cell(0, 1)
        self.assertEqual(board.get_bit(0), 1)
        self.assertEqual(board.get_bit(1), 0)

    def test_return_board(self):
        board = Bitboard()
        for index, value in ((0, 1), (1, 2), (2, 3), (3, 4)):
            board = board.set_cell(index, value)

        expected_board_value = (
            (1 << (0 * 4)) | (2 << (1 * 4)) | (3 << (2 * 4)) | (4 << (3 * 4))
        )
        self.assertEqual(board.return_board(), expected_board_value)

    def test_get_empty_cells(self):
        board = Bitboard()
        for index in range(16):
            if index % 2 == 0:
                board = board.set_cell(index, 1)

        empty_cells = board.get_empty_cells()
        expected_empty_cells = [i for i in range(16) if i % 2 != 0]
        self.assertEqual(empty_cells, expected_empty_cells)

    # def test_game_over_check(self): # fails
    #    board = Bitboard()
    #    for index in range(16):
    #        board = board.set_cell(index, 1)
    #
    #    self.assertTrue(board.game_over_check())
    #
    #    board = Bitboard()
    #    board = board.set_cell(0, 1)
    #    self.assertFalse(board.game_over_check())

    def test_move_invalid_direction(self):
        board = Bitboard()
        with self.assertRaises(ValueError):
            board.move("west")

    def test_move_line(self):
        self.assertEqual(Bitboard._move_line([1, 0, 2, 0]), [1, 2, 0, 0])
        self.assertEqual(Bitboard._move_line([2, 2, 0, 0]), [3, 0, 0, 0])
        self.assertEqual(Bitboard._move_line([4, 4, 4, 4]), [5, 5, 0, 0])
        self.assertEqual(
            Bitboard._move_line([8, 8, 16, 16]), [9, 17, 0, 0])

    def test_set_and_get_row(self):
        pass  # WIP

    def test_move_rows_left(self):
        board = Bitboard()
        for index, value in ((0, 1), (1, 1), (2, 2), (3, 2)):
            board = board.set_cell(index, value)

        moved_board = board.move("left")
        self.assertEqual(moved_board.get_cell(0), 2)
        self.assertEqual(moved_board.get_cell(1), 3)
        self.assertEqual(moved_board.get_cell(2), 0)
        self.assertEqual(moved_board.get_cell(3), 0)

    def test_move_rows_right(self):
        board = Bitboard()
        for index, value in ((0, 1), (1, 1), (2, 2), (3, 2)):
            board = board.set_cell(index, value)

        moved_board = board.move("right")
        self.assertEqual(moved_board.get_cell(0), 0)
        self.assertEqual(moved_board.get_cell(1), 0)
        self.assertEqual(moved_board.get_cell(2), 2)
        self.assertEqual(moved_board.get_cell(3), 3)

    def test_move_columns_up(self):
        board = Bitboard()
        for index, value in ((0, 1), (4, 1), (8, 2), (12, 2)):
            board = board.set_cell(index, value)

        moved_board = board.move("up")
        self.assertEqual(moved_board.get_cell(0), 2)
        self.assertEqual(moved_board.get_cell(4), 3)
        self.assertEqual(moved_board.get_cell(8), 0)
        self.assertEqual(moved_board.get_cell(12), 0)

    def test_move_columns_down(self):
        board = Bitboard()
        for index, value in ((0, 1), (4, 1), (8, 2), (12, 2)):
            board = board.set_cell(index, value)

        moved_board = board.move("down")
        self.assertEqual(moved_board.get_cell(0), 0)
        self.assertEqual(moved_board.get_cell(4), 0)
        self.assertEqual(moved_board.get_cell(8), 2)
        self.assertEqual(moved_board.get_cell(12), 3)
