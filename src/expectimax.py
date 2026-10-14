from bitboard import Bitboard
from heuristics import Heuristics


class Expectimax:
    def __init__(self, min_depth: int, max_depth: int):
        if not (2 <= min_depth <= max_depth <= 6):
            raise ValueError("Minimum depth must be between 2 and 6, and max depth must be between minimum depth and 6.")
        self.transposition_table: dict[tuple[str, int, int], float] = {}
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.heuristics = Heuristics()

    def get_search_depth(self, board: Bitboard) -> int:
        """Choose a deeper search as the number of empty cells decreases."""
        empty_cells = len(board.get_empty_cells())

        if empty_cells > 10:
            target_depth = 3
        elif empty_cells > 6:
            target_depth = 4
        elif empty_cells > 2:
            target_depth = 5
        else:
            target_depth = 6

        return max(self.min_depth, min(target_depth, self.max_depth))

    def expectimax(self, board: Bitboard, depth: int | None = None) -> float:
        """Returns the expected score of a board position using the expectimax algorithm."""
        if depth is None:
            depth = self.depth

        if depth <= 0:
            return self.heuristics.evaluate(board)

        key = ("max", board.return_board(), depth)
        if key in self.transposition_table:
            return self.transposition_table[key]

        best_score = float("-inf")

        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return self.heuristics.evaluate(board)

        for _, moved_board in valid_moves:
            if depth == 1:
                score = self.heuristics.evaluate(moved_board)
            else:
                score = self.expectimax_chance_node(moved_board, depth)
            best_score = max(best_score, score)

        self.transposition_table[key] = best_score
        return best_score

    def get_best_move(self, board: Bitboard) -> str | None:
        """Returns the valid move with the highest expected score."""
        self.transposition_table.clear()
        search_depth = self.get_search_depth(board)
        best_move = None
        best_score = float("-inf")

        for direction, moved_board in self.get_valid_moves(board):
            if search_depth == 1:
                score = self.heuristics.evaluate(moved_board)
            else:
                score = self.expectimax_chance_node(moved_board, search_depth)
            if score > best_score:
                best_score = score
                best_move = direction

        return best_move

    @staticmethod
    def get_valid_moves(board: Bitboard) -> list[tuple[str, Bitboard]]:
        """Return a list of valid moves for the given board."""
        current_board = board.return_board()
        valid_moves = []

        for direction in ("left", "right", "up", "down"):
            moved_board = board.move(direction)
            if moved_board.return_board() != current_board:
                valid_moves.append((direction, moved_board))

        return valid_moves

    def expectimax_chance_node(self, board: Bitboard, depth: int) -> float:
        """Returns the expected score of a chance node in the expectimax tree."""
        if depth <= 0:
            return self.heuristics.evaluate(board)

        #key = ("chance", board.return_board(), depth)
        #if key in self.transposition_table:
        #    return self.transposition_table[key]

        #if board.game_over_check():
        #    return self.heuristics.evaluate(board)

        total_score = 0.0

        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return self.heuristics.evaluate(board)

        empty_cells_len = len(empty_cells)

        for cell in empty_cells:
            for value, probability in ((1, 0.9), (2, 0.1)):
                new_board = board.set_cell(cell, value)
                score = self.expectimax(new_board, depth - 1)
                total_score += score * probability / empty_cells_len

        #self.transposition_table[key] = total_score
        return total_score
