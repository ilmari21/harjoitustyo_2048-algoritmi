from time import perf_counter
from expectimax import Expectimax
from game_2048 import Game2048

def main():
    depth = int(input("Enter the search depth for the AI (between 1 and 4, default is 4): ") or 4)
    game = Game2048()
    ai_2048 = Expectimax(depth=depth)
    moves = 0
    start_time = perf_counter()

    while True:
        direction = ai_2048.get_best_move(game.board)

        if direction is None:
            break

        if not game.move(direction):
            break

        moves += 1
        print(f"\nMove {moves}: {direction}")
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
