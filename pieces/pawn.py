from pieces.piece import Piece
from type import PieceType, TeamType


class Pawn(Piece):
    """
    Represents a Pawn piece in a chess game. Inherits from the Piece class.
    
    The Pawn class is a subclass of the Piece class, with a specific type of PieceType.PAWN.
    
    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p').
        type (PieceType): The type of the piece (PAWN).
    """
    
    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Pawn with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'P' if is_white else 'p'
        super().__init__(x, y, team, is_white, symbol, PieceType.PAWN)
