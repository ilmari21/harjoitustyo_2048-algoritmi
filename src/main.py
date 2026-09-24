from game_2048 import Game2048

def main():
    game = Game2048()
    print("Gameboard:")
    print(game.board)
    move_directions = {"w": "up", "a": "left", "s": "down", "d": "right"}

    while not game.board.game_over_check():
        move = input("Enter move (w/a/s/d): ").strip().lower()
        if move in move_directions:
            if game.move(move_directions[move]):
                print("Gameboard:")
                print(game.board)
            else:
                print("Invalid move. Try again.")
        else:
            print("Invalid input. Use w/a/s/d for moves.")

    print("Gameboard:")
    print(game.board)
    print("Game over!")

if __name__ == "__main__":
    main()
