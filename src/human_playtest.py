from game_2048 import Game2048


def display_board(game):
    """Display the current game board."""

    print("Gameboard:")
    print(game.board)


def human_playtest():
    """Run an interactive console game for a human player."""

    game = Game2048()
    display_board(game)
    move_directions = {"w": "up", "a": "left", "s": "down", "d": "right"}
    moves = 0

    while not game.board.game_over_check():
        move = input("Enter move (w/a/s/d): ").strip().lower()
        if move in move_directions:
            if game.move(move_directions[move]):
                moves += 1
                print(f"\nMove {moves}")
                print(f"Score: {game.score}")
                display_board(game)
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Use w/a/s/d for moves.")

    print(f"\nGame over after {moves} moves.")
    print(f"Final Score: {game.score}")
    display_board(game)


if __name__ == "__main__":
    human_playtest()
