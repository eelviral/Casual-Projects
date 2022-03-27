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
    """

    def __init__(self, x, y, piece=None):
        self._piece = piece
        self._x = x
        self._y = y

    @property
    def piece(self) -> Piece | None:
        """Get or set Chess piece

        Returns: Piece or None
        """
        return self._piece

    @piece.setter
    def piece(self, value):
        if type(value) == Piece:
            self._piece = value
        elif value is None:
            self._piece = None
        else:
            raise TypeError("piece must be a Piece object or None")

    @property
    def x(self) -> int:
        """Get or set x-coordinate (row)

        Returns: int
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self) -> int:
        """Get or set y-coordinate (column)

        Returns: int
        """
        return self._x

    @y.setter
    def y(self, value):
        self._y = value

    def __str__(self):
        return f"{self._piece} {self._x} {self._y}"
