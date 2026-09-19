from functools import cache
from move_logic import move_line

CELL_CONSTANT = 0xF


def _pack_line(cells: list[int]) -> int:
    """Pack four 4-bit cells into a single 16-bit integer."""
    return sum(
        (cell & CELL_CONSTANT) << (index * 4)
        for index, cell in enumerate(cells)
    )

def _move_packed_line(line: int, reverse: bool = False) -> int:
    """Move and merge a packed line of 4 cells."""
    cells = [(line >> (index * 4)) & CELL_CONSTANT for index in range(4)]
    return _pack_line(move_line(cells, reverse))

@cache
def _init_lookup_tables():
    return {
        'row_left': [_move_packed_line(row) for row in range(65536)],
        'row_right': [_move_packed_line(row, reverse=True) for row in range(65536)],
        'col_up': [_move_packed_line(column) for column in range(65536)],
        'col_down': [_move_packed_line(column, reverse=True) for column in range(65536)],
    }

def get_lookup_tables():
    """Return the lookup tables for moving rows and columns."""
    return _init_lookup_tables()
