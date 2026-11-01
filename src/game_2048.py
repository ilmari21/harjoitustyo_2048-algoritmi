import random
from bitboard import Bitboard


class Game2048:
    """Class representing the 2048 game logic, including board state, score, and tile spawning."""

    def __init__(self, rng: random.Random | None = None):
        """Constructor of the class; initializes the game with a random number generator and sets up the initial board state.

        Args:
            rng (random.Random | None): An optional random number generator for reproducibility. If None, a new random generator is created.
        """

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
        """Place a 2 (90% chance) or 4 (10% chance) in a random empty cell.

        Returns:
            True if a tile was successfully placed, False if there are no empty cells.
        """

        empty_cells = self.board.get_empty_cells()
        if not empty_cells:
            return False

        cell = self.rng.choice(empty_cells)
        exponent = 1 if self.rng.random() < 0.9 else 2
        self.board = self.board.set_cell(cell, exponent)
        return True

    def move(self, direction: str) -> bool:
        """Execute a move and update the board if it changes.

        Args:
            direction (str): The direction to move the tiles ('up', 'down', 'left', 'right').

        Returns:
            True if the board was updated, False otherwise.
        """

        moved_board = self.board.move(direction)

        if moved_board.return_board() == self.board.return_board():
            return False

        self.score += self._tile_score(moved_board) - \
            self._tile_score(self.board)
        self.board = moved_board
        self.spawn_random_tile()
        return True

    def get_board(self) -> int:
        """Return the current board state as a 64-bit integer.

        Returns:
            The 64-bit integer representing the game board.
        """

        return self.board.return_board()

    @staticmethod
    def _tile_score(board: Bitboard) -> int:
        """Calculate the total score represented by the board's tiles.

        Args:
            board (Bitboard): The board after the move.

        Returns:
            The score gained from the move.
        """

        score = 0
        for i in range(16):
            exponent = board.get_cell(i)
            if exponent > 1:
                score += (2 ** exponent) * (exponent - 1)
        return score
