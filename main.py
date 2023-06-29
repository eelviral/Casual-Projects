# Name: Chess Game Project
# Author: Eddie Elvira (@eelviral)
# Github_Link: https://github.com/eelviral/Chess-Game-Project
# Date_Created: Monday, March 7, 2022 at 05:51 UTC


from board import Board
from game_state import GameState
# from player import Human, Computer
# from ai import find_best_move
from ui.chess_ui import ChessUI


class Main:
    @staticmethod
    def start_game():
        # white = Human(white_side=True)
        # black = Computer(white_side=False)
        board = Board()
        game_state = GameState(board)
        ui = ChessUI(game_state)
        ui.run()

    if __name__ == '__main__':
        start_game()