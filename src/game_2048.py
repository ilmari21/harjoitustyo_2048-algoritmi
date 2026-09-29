import random
from bitboard import Bitboard

class Game2048:
    def __init__(self, rng: random.Random | None = None):
        self.rng = rng if rng is not None else random.Random()
        self.board = Bitboard()
        self.score = 0
        self.reset()

    def reset(self):
        """Reset the game and place the two starting tiles."""
        self.board = Bitboard()
        self.score = 0
        self.spawn_random_tile()
        self.spawn_random_tile()

    def spawn_random_tile(self) -> bool:
        """Place a 2 (90% chance) or 4 (10% chance) in a random empty cell."""
        empty_cells = self.board.get_empty_cells()
        if not empty_cells:
            return False

        cell = self.rng.choice(empty_cells)
        exponent = 1 if self.rng.random() < 0.9 else 2
        self.board = self.board.set_cell(cell, exponent)
        return True

    def move(self, direction: str) -> bool:
        """Execute a move and update the board if it changes."""
        moved_board = self.board.move(direction)

        if moved_board.return_board() == self.board.return_board():
            return False

        self.score += self._tile_score(moved_board) - self._tile_score(self.board)
        self.board = moved_board
        self.spawn_random_tile()
        return True

    def get_board(self) -> int:
        """Returns the board as an integer."""
        return self.board.return_board()

    def _tile_score(self, board: Bitboard) -> int:
        """Calculate the score gained from the move."""
        score = 0
        for i in range(16):
            exponent = board.get_cell(i)
            if exponent > 1:
                score += (2 ** exponent) * (exponent - 1)
        return score
