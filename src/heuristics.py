from bitboard import Bitboard


class Heuristics:
    SNAKE_WEIGHTS = (
        4 ** 15, 4 ** 14, 4 ** 13, 4 ** 12,
        4 ** 8, 4 ** 9, 4 ** 10, 4 ** 11,
        4 ** 7, 4 ** 6, 4 ** 5, 4 ** 4,
        4 ** 0, 4 ** 1, 4 ** 2, 4 ** 3,
    )
    EMPTY_CELL_WEIGHT = 100.0

    def evaluate(self, board: Bitboard) -> float:
        """Returns a score based on the evaluation."""
        empty_cells = 0
        snake_score = 0
        packed_board = board.return_board()

        for index, weight in enumerate(self.SNAKE_WEIGHTS):
            cell = (packed_board >> (index * 4)) & Bitboard.CELL_CONSTANT
            if cell == 0:
                empty_cells += 1
            snake_score += cell * weight

        return empty_cells * self.EMPTY_CELL_WEIGHT + snake_score
