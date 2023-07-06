from pieces import Piece
from type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_state import GameState


class Knight(Piece):
    """
    Represents a Knight piece in a chess game. Inherits from the Piece class.

    The Knight class is a subclass of the Piece class, with a specific type of PieceType.KNIGHT.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'N', 'n').
        type (PieceType): The type of the piece (KNIGHT).
    """

    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Knight with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'N' if is_white else 'n'
        super().__init__(x, y, team, is_white, symbol, PieceType.KNIGHT)

    def legal_move(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determine if a Knight's move is legal.

        Args:
            px (int): The current x-coordinate of the Knight.
            py (int): The current y-coordinate of the Knight.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        dx = abs(x - px)
        dy = abs(y - py)
        return ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)) and \
            self.can_capture_or_occupy_square(x, y, board=game_state.board)
