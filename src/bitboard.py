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
        tables = get_lookup_tables()
        table = tables[table_name]
        board = Bitboard()

        for row in range(4):
            board = board.set_row(row, table[self.get_row(row)])

        return board

    def _move_columns(self, table_name: str) -> 'Bitboard':
        table = get_lookup_tables()[table_name]
        board = Bitboard()

        for column in range(4):
            packed = sum(
                self.get_cell(row * 4 + column) << (row * 4)
                for row in range(4)
            )
            moved = table[packed]

            for row in range(4):
                cell = (moved >> (row * 4)) & self.CELL_CONSTANT
                board = board.set_cell(row * 4 + column, cell)

        return board

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
