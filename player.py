class Player:
    """A parent class used to represent a Player side on a chessboard

    Attributes
    ----------
    _is_white_side : bool
        Determines if the Player is using the white or black pieces
    _is_human: bool
        Determines if the Player is a human or computer player
    """
    def __init__(self, white_side):
        self._is_white_side = white_side
        self._is_human = None

    @property
    def is_white_side(self) -> bool:
        """Get or set a player's Chess piece color

        Returns: bool
            - True if player is on the white side of the chessboard
            - False if player is on the black side of the chessboard
        """
        return self._is_white_side

    @is_white_side.setter
    def is_white_side(self, value):
        if type(value) == bool:
            self._is_white_side = value
        else:
            raise TypeError("is_white_side must be a boolean")

    @property
    def is_human(self) -> bool:
        """Get or set if player is human

        Returns: bool
            - True if the player is human
            - False if the player is a computer
        """
        if self._is_human is None:
            raise Exception("is_human status cannot be NoneType,"
                            " and must be set before the game begins")
        return self._is_human

    @is_human.setter
    def is_human(self, value):
        if type(value) == bool:
            self._is_human = value
        else:
            raise TypeError("is_human must be a boolean")


class Human(Player):
    def __init__(self, white_side):
        super().__init__(white_side)
        self.is_human = True


class Computer(Player):
    def __init__(self, white_side):
        super().__init__(white_side)
        self.is_human = False
