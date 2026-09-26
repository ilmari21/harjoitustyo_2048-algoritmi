from expectimax import Expectimax
from game_2048 import Game2048

def main():
    game = Game2048()
    ai = Expectimax(depth=3)
    moves = 0

    while not game.board.game_over_check():
        direction = ai.get_best_move(game.board)

        if direction is None:
            break

        if not game.move(direction):
            break

        moves += 1
        print(f"\nMove {moves}: {direction}")
        print("Gameboard:")
        print(game.board)

    print(f"\nGame over after {moves} moves.")
    print("Gameboard:")
    print(game.board)

if __name__ == "__main__":
    main()
