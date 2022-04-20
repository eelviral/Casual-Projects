class Piece:
    """A parent class used to represent a Piece on a chessboard

    Attributes
    ----------
    _is_white : bool
        Determines if the Piece is white or black
    _name : str
        Name of the Piece
    _captured : bool
        Determines if the Piece is captured or not
    _moves_made : int
        Number of moves made by Piece
    """

    def __init__(self, white):
        self._is_white = white
        self._name = type(self).__name__
        self._captured = False
        self._moves_made = 0

    @property
    def is_white(self) -> bool:
        """Get or set the current Chess piece color

        Returns: bool
            - True if piece is white
            - False if piece is black
        """
        return self._is_white

    @is_white.setter
    def is_white(self, value) -> None:
        if type(value) == bool:
            self._is_white = value
        else:
            raise TypeError("is_white must be a boolean")

    @property
    def name(self) -> str:
        """Get the name of Chess piece

        Returns: str
        """
        return self._name

    @property
    def captured(self) -> bool:
        """Get or set capture status of Chess piece

        Returns: bool
            - True if piece is captured
            - False if piece is not captured
        """
        return self._captured

    @captured.setter
    def captured(self, value) -> None:
        if type(value) == bool:
            self._captured = value
        else:
            raise TypeError("captured must be a boolean")

    @property
    def moves_made(self) -> int:
        """Get or set the amount of moves made by a piece

        Returns: int
        """
        return self._moves_made

    @moves_made.setter
    def moves_made(self, value) -> None:
        if isinstance(value, int):
            self._moves_made = value
        else:
            raise TypeError("moves_made must be an integer")

    def can_move(self, board, start, end): _abstract()

    def controlled_squares(self, board, x, y): _abstract()

    def __repr__(self):
        if self.is_white:
            return f"White {type(self).__name__}"
        else:
            return f"Black {type(self).__name__}"

    def __str__(self):
        piece_symbols = {
            'Bishop': 'B',
            'King': 'K',
            'Knight': 'N',
            'Pawn': 'P',
            'Queen': 'Q',
            'Rook': 'R'
        }
        if self.is_white:
            color = 'w'
        else:
            color = 'b'

        return color + piece_symbols.get(type(self).__name__.lower().capitalize())


def _abstract():
    raise NotImplementedError


def override(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider
