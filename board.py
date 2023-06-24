from type import TeamType
from pieces import *


class Board:
    """
    A class used to represent a Chess Board.

    Attributes:
        board (list): A list of Piece objects representing the current state of the chess board.
    """

    def __init__(self):
        """
        Initializes a Board with an empty list and calls the method to initialize the board with pieces.
        """
        self.board = []
        self._initialize_board()
    
    def _initialize_board(self):
        """
        Initializes the board with chess pieces in their starting positions.
        The board is represented as a list of Piece objects.
        """
        # Add non-pawn pieces
        for p in range(2):
            team_type = TeamType.OPPONENT if p == 0 else TeamType.ALLY
            is_white = False if team_type == TeamType.OPPONENT else True
            y = 0 if team_type == TeamType.OPPONENT else 7

            self.board.append(Rook(x=0, y=y, team=team_type, is_white=is_white))
            self.board.append(Knight(x=1, y=y, team=team_type, is_white=is_white))
            self.board.append(Bishop(x=2, y=y, team=team_type, is_white=is_white))
            self.board.append(Queen(x=3, y=y, team=team_type, is_white=is_white))
            self.board.append(King(x=4, y=y, team=team_type, is_white=is_white))
            self.board.append(Bishop(x=5, y=y, team=team_type, is_white=is_white))
            self.board.append(Knight(x=6, y=y, team=team_type, is_white=is_white))
            self.board.append(Rook(x=7, y=y, team=team_type, is_white=is_white))

        # Add pawns
        for i in range(8):
            self.board.append(Pawn(x=i, y=1, team=TeamType.OPPONENT, is_white=False))
            self.board.append(Pawn(x=i, y=6, team=TeamType.ALLY, is_white=True))

    def __getitem__(self, index):
        """
        Returns the Piece object at the given index in the board list.

        Args:
            index (int): The index of the piece in the board list.

        Returns:
            Piece: The Piece object at the given index.
        """
        return self.board[index]
