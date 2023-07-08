from utils.type import TeamType
from pieces import *


class Board:
    """
    A class used to represent a Chess Board.

    Attributes:
        pieces (list): A list of Piece objects representing the current state of the chess board.
                       Each object stores information about the type of the piece, its location on 
                       the board, the team it belongs to, and its color.
    """

    def __init__(self):
        """
        Initializes a Board with an empty list of pieces and calls the method 
        to populate the board with chess pieces in their starting positions.
        """
        self._pieces = []
        self._initialize_board()

    def __getitem__(self, index: int) -> Piece:
        """
        Returns the Piece object at the given index in the board list.

        Args:
            index (int): The index of the piece in the board list.

        Returns:
            Piece: The Piece object at the given index.
        """
        return self.pieces[index]

    def __getattr__(self, name) -> list[Piece]:
        """
        Returns the value of the attribute named "name".

        Args:
            name (str): The name of the attribute.

        Returns:
            list: If name is "board", returns the list of pieces on the board.

        Raises:
            AttributeError: If name is not "board".
        """
        if name == "board":
            return self.pieces
        raise AttributeError(f"'Board' object has no attribute '{name}'")

    @property
    def pieces(self) -> list[Piece]:
        """
        Returns the list of Piece objects representing the current state of the chess board.

        Returns:
            list: A list of Piece objects.
        """
        return self._pieces

    def piece_at(self, x: int, y: int) -> Piece or None:
        """
        Returns the piece at a given position on the board.

        Args:
            x (int): The x-coordinate of the position on the board.
            y (int): The y-coordinate of the position on the board.

        Returns:
            Piece or None: If there's a piece at the given position, it returns the Piece object.
                           If there's no piece at the position, it returns None.
        """
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def get_king(self, team: TeamType) -> King:
        """
        Returns the king piece of the given team.

        Args:
            team (TeamType): The team whose king to return.

        Returns:
            King: The king of the given team.
        """
        for piece in self.pieces:
            if isinstance(piece, King) and piece.team == team:
                return piece

    def add(self, piece: Piece):
        """
        Adds a piece to the board.

        Args:
            piece (Piece): The piece to be added to the board.
        """
        self.pieces.append(piece)

    def remove(self, piece: Piece):
        """
        Removes a piece from the board.

        Args:
            piece (Piece): The piece to be removed from the board.
        """
        self.pieces.remove(piece)

    def _initialize_board(self):
        """
        Populates the board with chess pieces in their initial positions.

        The method creates objects of various piece types (Rook, Knight, Bishop, Queen, King, and Pawn)
        and places them on the board as per the traditional setup of a chess game.

        The board is represented as a list of Piece objects, with each object storing information
        about the type of the piece, its location on the board, the team it belongs to, and its color.
        """
        # Add non-pawn pieces
        for p in range(2):
            team_type = TeamType.OPPONENT if p == 0 else TeamType.ALLY
            is_white = False if team_type == TeamType.OPPONENT else True
            y = 0 if team_type == TeamType.OPPONENT else 7

            self.add(Rook(x=0, y=y, team=team_type, is_white=is_white))
            self.add(Knight(x=1, y=y, team=team_type, is_white=is_white))
            self.add(Bishop(x=2, y=y, team=team_type, is_white=is_white))
            self.add(Queen(x=3, y=y, team=team_type, is_white=is_white))
            self.add(King(x=4, y=y, team=team_type, is_white=is_white))
            self.add(Bishop(x=5, y=y, team=team_type, is_white=is_white))
            self.add(Knight(x=6, y=y, team=team_type, is_white=is_white))
            self.add(Rook(x=7, y=y, team=team_type, is_white=is_white))

        # Add pawns
        for i in range(8):
            self.add(Pawn(x=i, y=1, team=TeamType.OPPONENT, is_white=False))
            self.add(Pawn(x=i, y=6, team=TeamType.ALLY, is_white=True))
