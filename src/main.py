from time import perf_counter
from expectimax import Expectimax
from game_2048 import Game2048


def main():
    min_depth = int(input(
        "Enter the minimum search depth for the AI (2-6, default is 2): ") or 2)
    max_depth = int(input(
        f"Enter the maximum search depth for the AI ({min_depth}-6, default is 6): ") or 6)
    game = Game2048()
    ai_2048 = Expectimax(min_depth, max_depth)
    moves = 0
    start_time = perf_counter()

    while True:
        search_depth = ai_2048.get_search_depth(game.board)
        direction = ai_2048.get_best_move(game.board)

        if direction is None:
            break

        if not game.move(direction):
            break

        moves += 1
        print(f"\nMove {moves}: {direction} (search depth: {search_depth})")
        print(f"Score: {game.score}")
        print("Gameboard:")
        print(game.board)

    _game_summary(game, moves, start_time)


def _game_summary(game: Game2048, moves: int, start_time: float) -> None:
    elapsed_seconds = int(perf_counter() - start_time)
    minutes, seconds = divmod(elapsed_seconds, 60)
    print(f"\nGame over after {moves} moves.")
    print(f"Elapsed time: {minutes:02d}:{seconds:02d}")
    print(f"Final Score: {game.score}")
    print("Gameboard:")
    print(game.board)


if __name__ == "__main__":
    main()
