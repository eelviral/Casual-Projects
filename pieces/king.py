from pieces import Piece
from type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board


class King(Piece):
    """
    Represents a King piece in a chess game. Inherits from the Piece class.
    
    The King class is a subclass of the Piece class, with a specific type of PieceType.KING.
    
    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'K', 'k').
        type (PieceType): The type of the piece (KING).
    """
    
    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a King with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'K' if is_white else 'k'
        super().__init__(x, y, team, is_white, symbol, PieceType.KING)
        
    def legal_move(self, px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Determine if a King's move is legal.

        Args:
            px (int): The current x-coordinate of the King.
            py (int): The current y-coordinate of the King.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        dx = abs(x - px)
        dy = abs(y - py)
        return (dx <= 1 and dy <= 1) and self._can_capture_or_occupy_square(x, y, board)