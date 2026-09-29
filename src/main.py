from expectimax import Expectimax
from game_2048 import Game2048

def main():
    depth = int(input("Enter the depth for the Expectimax AI (1-3): "))
    game = Game2048()
    ai = Expectimax(depth=depth)
    moves = 0

    while not game.board.game_over_check():
        direction = ai.get_best_move(game.board)

        if direction is None:
            break

        if not game.move(direction):
            break

        moves += 1
        print(f"\nMove {moves}: {direction}")
        print(f"Score: {game.score}")
        print("Gameboard:")
        print(game.board)

    print(f"\nGame over after {moves} moves.")
    print(f"Final Score: {game.score}")
    print("Gameboard:")
    print(game.board)

if __name__ == "__main__":
    main()
