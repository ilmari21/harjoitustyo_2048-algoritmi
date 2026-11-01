from statistics import median
from time import perf_counter

from expectimax import Bitboard, Expectimax

board = Bitboard()
for index, value in ((0, 7), (1, 7), (2, 1)):
    board = board.set_cell(index, value)

for depth in (2, 3, 4, 5, 6):
    times = []
    move = None

    for _ in range(3):
        ai = Expectimax(min_depth=depth, max_depth=depth)
        start = perf_counter()
        move = ai.get_best_move(board)
        times.append(perf_counter() - start)

    print(f"depth={depth}, median={median(times):.3f}s, move={move}")
