from abc import abstractmethod
from type import PieceType, TeamType


class Piece:
    """
    A parent class used to represent a Piece on a chessboard.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black)
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p', 'N', 'n').
        type (PieceType): The type of the piece (e.g., PAWN, KNIGHT).
    """
    
    def __init__(self, x: int, y: int, team: TeamType, is_white: bool, symbol: str, type: PieceType):
        """
        Initializes a Piece with a symbol, coordinates, type, and team.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black)
            symbol (str): The character symbol representing the piece (e.g., 'P', 'p', 'N', 'n').
            type (PieceType): The type of the piece (e.g., PAWN, KNIGHT).
        """
        self._x = x
        self._y = y
        self._team = team
        self._is_white = is_white
        self._symbol = symbol
        self._type = type

    @property
    def x(self) -> int:
        """Returns the x-coordinate of the piece on the board."""
        return self._x

    @property
    def y(self) -> int:
        """Returns the y-coordinate of the piece on the board."""
        return self._y

    @property
    def team(self) -> TeamType:
        """Returns the team the piece belongs to."""
        return self._team
    
    @property
    def is_white(self) -> bool:
        """
        Returns the color of the piece.

        Returns:
            bool: True if the piece is white, False if the piece is black.
        """
        return self._is_white

    @property
    def symbol(self) -> str:
        """Returns the symbol of the piece."""
        return self._symbol
    
    @property
    def type(self) -> PieceType:
        """Returns the type of the piece."""
        return self._type
    