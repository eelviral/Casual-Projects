# Name: Chess Game Project
# Author: Eddie Elvira (@eelviral)
# Github_Link: https://github.com/eelviral/Chess-Game-Project
# Date_Created: Monday, March 7, 2022 at 05:51 UTC


from engine import GameState, Board, GameController
from ui import ChessUI


class Main:
    @staticmethod
    def start_game():
        board = Board()
        game_state = GameState(board)
        game_controller = GameController(game_state)
        ui = ChessUI(game_controller)
        ui.run()

    if __name__ == '__main__':
        start_game()
