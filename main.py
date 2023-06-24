# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC


from board import Board
from game_state import GameState
# from player import Human, Computer
# from ai import find_best_move
from ui import ChessUI

if __name__ == '__main__':
    # white = Human(white_side=True)
    # black = Computer(white_side=False)
    board = Board()
    game_state = GameState(board)
    ui = ChessUI(game_state)
    ui.run()
