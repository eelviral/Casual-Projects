from pieces import Piece
from type import PieceType, TeamType


class Rook(Piece):
    """
    Represents a Rook piece in a chess game. Inherits from the Piece class.
    
    The Rook class is a subclass of the Piece class, with a specific type of PieceType.ROOK.
    
    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'R', 'r').
        type (PieceType): The type of the piece (ROOK).
    """
    
    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Rook with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'R' if is_white else 'r'
        super().__init__(x, y, team, is_white, symbol, PieceType.ROOK)
        
    def legal_move(self, px: int, py: int, x: int, y: int):
        return px == x or py == y
    