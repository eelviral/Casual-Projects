from board import Board


class GameState:
    """
    A class used to represent the current state of a Chess game.

    Attributes:
        board (Board): A Board object representing the current state of the chess board.
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a given Board object.

        Args:
            board (Board): A Board object representing the current state of the chess board.
        """
        self.board = board
