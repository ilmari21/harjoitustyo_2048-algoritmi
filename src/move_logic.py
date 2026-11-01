def move_line(cells: list[int], reverse: bool = False) -> list[int]:
    """Move and merge four cells.

    Args:
        cells (list[int]): A list of four 4-bit exponents.
        reverse (bool): Whether to process the cells in reverse order.

    Returns:
        A list of four 4-bit exponents representing the moved and merged cells.
    """

    if reverse:
        cells = cells[::-1]

    compact_cells = [cell for cell in cells if cell != 0]
    merged = []
    index = 0
    while index < len(compact_cells):
        if index + 1 < len(compact_cells) and compact_cells[index] == compact_cells[index + 1]:
            merged.append(compact_cells[index] + 1)
            index += 2
        else:
            merged.append(compact_cells[index])
            index += 1

    result = merged + [0] * (4 - len(merged))
    if reverse:
        result = result[::-1]
    return result
