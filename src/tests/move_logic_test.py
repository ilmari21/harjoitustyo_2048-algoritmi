import unittest
from move_logic import move_line

class TestMoveLine(unittest.TestCase):
    def test_move_line_no_merge(self):
        self.assertEqual(move_line([1, 0, 2, 0]), [1, 2, 0, 0])
        self.assertEqual(move_line([2, 0, 0, 4]), [2, 4, 0, 0])
        self.assertEqual(move_line([8, 16, 32, 64]), [8, 16, 32, 64])

    def test_move_line_with_merge(self):
        self.assertEqual(move_line([2, 2, 0, 0]), [3, 0, 0, 0])  
        self.assertEqual(move_line([4, 4, 4, 4]), [5, 5, 0, 0])  
        self.assertEqual(move_line([8, 8, 16, 16]), [9, 17, 0, 0])

    def test_move_line_reverse(self):
        self.assertEqual(move_line([0, 0, 2, 2], reverse=True), [0, 0, 0, 3])  
        self.assertEqual(move_line([4, 4, 4, 4], reverse=True), [0, 0, 5, 5])  
        self.assertEqual(move_line([16, 16, 8, 8], reverse=True), [0, 0, 17, 9])
