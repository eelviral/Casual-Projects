# Name: Chess Game Project
# Author: Eddie Elvira (@eelviral)
# Github_Link: https://github.com/eelviral/Chess-Game-Project
# Date_Created: Monday, March 7, 2022 at 05:51 UTC


from engine import ChessGame
from ui import ChessUI


class Main:
    @staticmethod
    def start_game():
        chess_game = ChessGame()
        ui = ChessUI(chess_game)
        ui.run()

    if __name__ == '__main__':
        start_game()
