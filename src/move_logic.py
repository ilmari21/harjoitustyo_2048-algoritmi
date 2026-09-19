def move_line(cells: list[int], reverse: bool = False) -> list[int]:
    """Move and merge 4 cells."""
    if reverse:
        cells.reverse()

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
        result.reverse()
    return result
