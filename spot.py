from piece import Piece


class Spot:
    """A class used to represent a Spot on a chessboard

    Attributes
    ----------
    x : int
        x-coordinate (row) on the chessboard
    y : int
        y-coordinate (column) on the chessboard
    piece : Piece
        the Piece currently positioned at this Spot
    _controlled_squares : list
        the squares controlled by this Spot
    """

    def __init__(self, x, y, piece=None):
        self._piece = piece
        self._x = x
        self._y = y
        self._controlled_squares = None

    @property
    def piece(self) -> Piece:
        """Get or set Chess piece

        Returns: Piece
        """
        return self._piece

    @piece.setter
    def piece(self, value) -> None:
        if isinstance(value, Piece):
            self._piece = value
        elif value is None:
            self._piece = None
        else:
            raise TypeError("piece must be a Piece or NoneType")
        
    @property
    def controlled_squares(self) -> list:
        """Get or set the list of squares controlled by the Piece at this Spot

        Returns: list
        """
        return self._controlled_squares

    @controlled_squares.setter
    def controlled_squares(self, value) -> None:
        if isinstance(value, list):
            self._controlled_squares = value
        elif value is None:
            self._controlled_squares = []
        else:
            raise TypeError("controlled_squares must be a list")

    @property
    def x(self) -> int:
        """Get or set x-coordinate (row)

        Returns: int
        """
        return self._x

    @x.setter
    def x(self, value) -> None:
        if isinstance(value, int):
            self._x = value
        else:
            raise TypeError("x must be an int")

    @property
    def y(self) -> int:
        """Get or set y-coordinate (column)

        Returns: int
        """
        return self._y

    @y.setter
    def y(self, value) -> None:
        if isinstance(value, int):
            self._y = value
        else:
            raise TypeError("y must be an int")

    def __str__(self):
        return f"{self._piece} {self._x} {self._y}"
