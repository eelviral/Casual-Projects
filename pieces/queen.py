from pieces import Piece
from type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_state import GameState


class Queen(Piece):
    """
    Represents a Queen piece in a chess game. Inherits from the Piece class.

    The Queen class is a subclass of the Piece class, with a specific type of PieceType.QUEEN.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'Q', 'q').
        type (PieceType): The type of the piece (QUEEN).
    """

    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Queen with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'Q' if is_white else 'q'
        super().__init__(x, y, team, is_white, symbol, PieceType.QUEEN)

    def legal_move(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determine if a Queen's move is legal.

        Args:
            px (int): The current x-coordinate of the Queen.
            py (int): The current y-coordinate of the Queen.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if not self.can_capture_or_occupy_square(x, y, board=game_state.board):
            return False

        if px == x or py == y:
            return self._path_is_clear(px, py, x, y, board=game_state.board, direction='linear')
        elif abs(x - px) == abs(y - py):
            return self._path_is_clear(px, py, x, y, board=game_state.board, direction='diagonal')

        return False
