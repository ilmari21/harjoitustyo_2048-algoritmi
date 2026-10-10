from lookup_tables import get_lookup_tables
from move_logic import move_line


class Bitboard:
    CELL_CONSTANT = 0xF
    BOARD_CONSTANT = (1 << 64) - 1
    ROW_CONSTANT = (1 << 16) - 1

    def __init__(self, board: int = 0):
        self.board: int = board & self.BOARD_CONSTANT

    def get_cell(self, index: int) -> int:
        """Returns the 4-bit exponent stored in a cell."""
        return (self.board >> (index * 4)) & self.CELL_CONSTANT

    def set_cell(self, index: int, value: int) -> 'Bitboard':
        """Returns a board with one 4-bit cell replaced."""
        cell_constant = self.CELL_CONSTANT << (index * 4)
        board = self.board & ~cell_constant
        board |= (value & self.CELL_CONSTANT) << (index * 4)
        return Bitboard(board)

    def get_bit(self, index: int) -> bool:
        """Returns boolean indicating if the bit is set or not."""
        return (self.board >> index) & 1 == 1

    def return_board(self) -> int:
        """Returns the board as an integer."""
        return self.board

    def get_empty_cells(self) -> list[int]:
        """Return the indexes of all empty cells."""
        return [index for index in range(16) if self.get_cell(index) == 0]

    def game_over_check(self) -> bool:
        """Checks whether it is possible to make any more moves on the board."""
        directions = ('left', 'right', 'up', 'down')
        return all(
            self.move(direction).return_board() == self.board
            for direction in directions
        )

    @staticmethod
    def _move_line(cells: list[int], reverse: bool = False) -> list[int]:
        """Move and merge four cells."""
        return move_line(cells, reverse)

    def get_row(self, index: int) -> int:
        """Return a row as a 16-bit value containing 4 packed cells."""
        return (self.board >> (index * 16)) & self.ROW_CONSTANT

    def set_row(self, index: int, row: int) -> 'Bitboard':
        """Return a board with 1 packed row replaced."""
        row_mask = self.ROW_CONSTANT << (index * 16)
        board = self.board & ~row_mask
        board |= (row & self.ROW_CONSTANT) << (index * 16)
        return Bitboard(board)

    def move(self, direction: str) -> 'Bitboard':
        """Execute the requested move and return the resulting board."""
        moves = {
            'left': self.move_left,
            'right': self.move_right,
            'up': self.move_up,
            'down': self.move_down,
        }

        try:
            return moves[direction]()
        except KeyError:
            raise ValueError(f"Invalid direction: {direction}") from None

    def move_left(self) -> 'Bitboard':
        """Moves the board left and returns a new Bitboard instance."""
        return self._move_rows('row_left')

    def move_right(self) -> 'Bitboard':
        """Move the board right and return a new Bitboard instance."""
        return self._move_rows('row_right')

    def move_up(self) -> 'Bitboard':
        """Moves the board up and returns a new Bitboard instance."""
        return self._move_columns('col_up')

    def move_down(self) -> 'Bitboard':
        """Moves the board down and returns a new Bitboard instance."""
        return self._move_columns('col_down')

    def _move_rows(self, table_name: str) -> 'Bitboard':
        """Move the rows of the board."""
        table = get_lookup_tables()[table_name]
        value = self.board
        moved_board = (
            table[value & self.ROW_CONSTANT]
            | (table[(value >> 16) & self.ROW_CONSTANT] << 16)
            | (table[(value >> 32) & self.ROW_CONSTANT] << 32)
            | (table[(value >> 48) & self.ROW_CONSTANT] << 48)
        )

        return Bitboard(moved_board)

    def _move_columns(self, table_name: str) -> 'Bitboard':
        """Move the columns of the board."""
        table = get_lookup_tables()[table_name]
        value = self.board
        moved_board = 0

        for column in range(4):
            shift = column * 4
            packed = (
                ((value >> shift) & self.CELL_CONSTANT)
                | (((value >> (shift + 16)) & self.CELL_CONSTANT) << 4)
                | (((value >> (shift + 32)) & self.CELL_CONSTANT) << 8)
                | (((value >> (shift + 48)) & self.CELL_CONSTANT) << 12)
            )
            moved_column = table[packed]
            moved_board |= (
                ((moved_column & self.CELL_CONSTANT) << shift)
                | (((moved_column >> 4) & self.CELL_CONSTANT) << (shift + 16))
                | (((moved_column >> 8) & self.CELL_CONSTANT) << (shift + 32))
                | (((moved_column >> 12) & self.CELL_CONSTANT) << (shift + 48))
            )

        return Bitboard(moved_board)

    def __str__(self) -> str:
        """Returns a string representation of the current board."""
        rows = []
        for row in range(4):
            cells = []
            for column in range(4):
                index = row * 4 + column
                exponent = self.get_cell(index)
                cells.append(str(0 if exponent == 0 else 1 << exponent))
            rows.append(" | ".join(f"{cell:>3}" for cell in cells))
        return "\n".join(rows)
