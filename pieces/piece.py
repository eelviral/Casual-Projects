from abc import ABC, abstractmethod
from utils.type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import GameState, Board


class Piece(ABC):
    """
    A parent class used to represent a Piece on a chessboard.

    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p', 'N', 'n').
        type (PieceType): The type of the piece (e.g., PAWN, KNIGHT).
        has_moved (bool): Determines whether the piece has already moved (at least once) or not.
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
        self._has_moved = False

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the Piece object.

        This method is mainly useful for debugging and logging. The string includes the piece's symbol,
        its x and y coordinates, its team, and whether it has moved or not.

        Returns:
            str: A string representation of the Piece object.
        """
        team = "White" if self.is_white else "Black"
        return f"Piece({self.symbol}, position=({self.x}, {self.y}), team={team}, has_moved={self.has_moved})"

    @property
    def x(self) -> int:
        """Returns the x-coordinate of the piece on the board."""
        return self._x

    @property
    def y(self) -> int:
        """Returns the y-coordinate of the piece on the board."""
        return self._y

    @x.setter
    def x(self, value: int):
        """
        Sets the x-coordinate of the piece on the board.

        Args:
            value (int): The new x-coordinate.
        """
        if not isinstance(value, int):
            raise TypeError("The x-coordinate must be an integer.")
        if not 0 <= value < 8:
            raise ValueError("The x-coordinate must be between 0 and 7.")
        self._x = value

    @y.setter
    def y(self, value: int):
        """
        Sets the y-coordinate of the piece on the board.

        Args:
            value (int): The new y-coordinate.
        """
        if not isinstance(value, int):
            raise TypeError("The y-coordinate must be an integer.")
        if not 0 <= value < 8:
            raise ValueError("The y-coordinate must be between 0 and 7.")
        self._y = value

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

    @property
    def has_moved(self) -> bool:
        """
        Checks whether the piece has moved at least once.

        Returns:
            bool: True if the piece has moved, False otherwise.
        """
        return self._has_moved

    @has_moved.setter
    def has_moved(self, value: bool):
        """
        Sets the piece's moved state.

        Args:
            value (bool): The new moved state of the piece.
        """
        self._has_moved = value

    @abstractmethod
    def legal_move(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Abstract method to determine whether a proposed move is legal, according to the rules of the piece.

        The implementation should take into account the piece's movement/capture patterns,
        as well as any potential obstructions or requirements of the game state.

        Parameters:
            px (int): The current x-coordinate of the piece.
            py (int): The current y-coordinate of the piece.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the move is legal, False otherwise.

        Raises:
            NotImplementedError: If this method is not overridden in a subclass.
        """
        raise NotImplementedError()

    def is_controlled_square(self, current_x: int, current_y: int, target_x: int, target_y: int,
                             game_state: 'GameState') -> bool:
        """
        Determines whether a proposed move to a target square on the chessboard is controlled by this piece.

        This method serves as a base for all piece-specific methods to follow and is designed to be overridden in
        subclasses. The specific rules for each piece, such as movement/capture patterns, obstructions on the path,
        and special game state requirements, should be considered in the overriding methods.

        Parameters:
            current_x (int): The current x-coordinate of this piece on the board.
            current_y (int): The current y-coordinate of this piece on the board.
            target_x (int): The x-coordinate of the proposed target square on the board.
            target_y (int): The y-coordinate of the proposed target square on the board.
            game_state (GameState): The current state of the chess game.

        Returns:
            bool: True if the proposed target square is controlled by this piece according to its specific rules;
                  False otherwise.
        """
        # This is a placeholder implementation that simply checks whether a legal move to the target square is possible.
        # Subclasses should override this method to implement more accurate rules for each piece if necessary.
        return self.legal_move(px=current_x, py=current_y, x=target_x, y=target_y, game_state=game_state)

    def can_capture_or_occupy_square(self, x: int, y: int, board: 'Board') -> bool:
        """
        Determine if a given piece can capture an opponent's piece at a specified square, 
        or occupy it if the square is empty.

        Parameters:
            x (int): The x-coordinate of the square.
            y (int): The y-coordinate of the square.
            board (Board): The game board.

        Returns:
            bool: True if the piece can capture or occupy the square, False otherwise.
        """
        destination_piece = board.piece_at(x, y)
        if destination_piece is None or destination_piece.is_white != self.is_white:
            return True
        return False

    def _path_is_clear(self, px: int, py: int, x: int, y: int, board: 'Board', direction: str) -> bool:
        """
        Determines whether the path is clear in a specified direction (linear or diagonal).

        Args:
            px (int): The current x-coordinate of the piece.
            py (int): The current y-coordinate of the piece.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.
            direction (str): The direction of movement. Can be either 'linear' or 'diagonal'.

        Returns:
            bool: True if the path in the specified direction is clear (i.e., there are no other pieces in the way),
                  False otherwise.

        Raises:
            ValueError: If the specified direction is not 'linear' or 'diagonal'.
        """
        if direction == 'linear':
            return self.__path_is_clear_linearly(px, py, x, y, board)
        elif direction == 'diagonal':
            return self.__path_is_clear_diagonally(px, py, x, y, board)
        else:
            raise ValueError(f"Invalid direction: {direction}")

    @staticmethod
    def __path_is_clear_diagonally(px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Determine whether the path is clear diagonally between two given points.
        This is intended for use by the Queen and Bishop subclasses.

        Args:
            px (int): The current x-coordinate of the piece.
            py (int): The current y-coordinate of the piece.
            x (int): The target x-coordinate.
            y (int): The target y-coordinate.
            board (Board): The current state of the game board.

        Returns:
            bool: True if the diagonal path is clear, False otherwise (i.e., if there are any pieces along the path).
        """
        if px != x and py != y:
            dx = 1 if x > px else -1
            dy = 1 if y > py else -1
            i, j = px + dx, py + dy
            while i != x and j != y:
                if board.piece_at(i, j) is not None:
                    return False
                i += dx
                j += dy
        return True

    @staticmethod
    def __path_is_clear_linearly(px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Determine whether the path is clear in a straight line (horizontally or vertically)
        between two given points. This is intended for use by the Queen and Rook subclasses.

        Args:
            px (int): The current x-coordinate of the piece.
            py (int): The current y-coordinate of the piece.
            x (int): The target x-coordinate.
            y (int): The target y-coordinate.
            board (Board): The current state of the game board.

        Returns:
            bool: True if the linear path is clear, False otherwise (i.e., if there are any pieces along the path).
        """
        if px == x or py == y:
            for i in range(min(px, x) + 1, max(px, x)):
                if board.piece_at(i, y) is not None:
                    return False
            for j in range(min(py, y) + 1, max(py, y)):
                if board.piece_at(x, j) is not None:
                    return False
        return True
