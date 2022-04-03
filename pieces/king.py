from piece import Piece, override


class King(Piece):
    def __init__(self, white):
        super().__init__(white)
        self._is_castling = False

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if king can currently move to marked position
        """

        x = abs(end.x - start.x)
        y = abs(end.y - start.y)

        # Don't move if same square
        if x == 0 and y == 0:
            return False
        
        if (x + y) == 1 or (x == 1 and y == 1):
            # If end position is empty, move
            if end.piece is None:
                return True

            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                return True

        return self.is_valid_castle(board, start, end)

    @property
    def is_castling(self) -> bool:
        """Get or set the king's castle status

        Returns: bool
            - True if king is castling
            - False if king is not castling
        """
        return self._is_castling

    @is_castling.setter
    def is_castling(self, value) -> None:
        if type(value) == bool:
            self._is_castling = value
        else:
            raise TypeError("is_castling must be a boolean")

    def is_valid_castle(self, board, start, end) -> bool:
        if self._is_castling:
            return False