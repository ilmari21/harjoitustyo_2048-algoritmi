from bitboard import Bitboard
from heuristics import Heuristics

class Expectimax:
    def __init__(self, depth):
        self.depth = depth
        self.heuristics = Heuristics()

    def expectimax(self, board: Bitboard, depth: int | None = None) -> float:
        """Returns the expected score of a board position using the expectimax algorithm."""
        if depth is None:
            depth = self.depth

        if depth <= 0 or board.game_over_check():
            return self.heuristics.evaluate(board)

        best_score = float("-inf")

        for direction in self.get_valid_moves(board):
            score = self.expectimax_chance_node(
                board.move(direction),
                depth
            )
            best_score = max(best_score, score)

        return best_score

    def get_best_move(self, board: Bitboard) -> str | None:
        """Returns the valid move with the highest expected score."""
        best_move = None
        best_score = float("-inf")

        for direction in self.get_valid_moves(board):
            score = self.expectimax_chance_node(
                board.move(direction),
                self.depth
            )
            if score > best_score:
                best_score = score
                best_move = direction

        return best_move

    def get_valid_moves(self, board: Bitboard) -> list[str]:
        """Return a list of valid moves for the given board."""
        valid_moves = []
        for direction in ('left', 'right', 'up', 'down'):
            if board.move(direction).return_board() != board.return_board():
                valid_moves.append(direction)
        return valid_moves

    def expectimax_chance_node(self, board: Bitboard, depth: int) -> float:
        """Returns the expected score of a chance node in the expectimax tree."""
        if depth <= 0 or board.game_over_check():
            return self.heuristics.evaluate(board)

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

        return total_score
