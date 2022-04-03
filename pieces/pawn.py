from piece import Piece, override


class Pawn(Piece):
    def __init__(self, white):
        super().__init__(white)
        self._is_promoted = False
        self._first_move = True

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if pawn can currently move to marked position
        """

        x = end.x - start.x
        y = abs(end.y - start.y)

        # Don't move if same square
        if x == 0 and y == 0:
            return False

        if self.first_move and y == 0:
            if ((self.is_white and x == 2 and start.x == 1) or
                    ((not self.is_white) and x == -2 and start.x == 6)):
                self.first_move = False
                return True
            else:
                self.first_move = False

        if not ((self.is_white and x == 1) or
                (not self.is_white) and x == -1):
            return False

        if y == 0:
            # If end position is empty, move
            if end.piece is None:
                return True
            else:
                return False
        elif abs(x) == 1 and y == 1:
            # Cannot "capture" an empty spot
            if end.piece is None:
                return False

            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                return True
        return self.is_valid_promotion(start, end)

    @property
    def is_promoted(self):
        """Get or set pawn promotion status

        Returns: bool
            - True if a pawn is being promoted
            - False if no pawn is being promoted
        """
        return self._is_promoted

    @is_promoted.setter
    def is_promoted(self, value):
        if type(value) == bool:
            self._is_promoted = value
        else:
            raise TypeError("is_promoted must be a boolean")
        
    @property
    def first_move(self):
        """Get or set first move status

        Returns: bool
            - True if a pawn is pending first move
            - False if no pawn already made its first move
        """
        return self._first_move

    @first_move.setter
    def first_move(self, value):
        if type(value) == bool:
            self._first_move = value
        else:
            raise TypeError("first_move must be a boolean")

    def is_valid_promotion(self, start, end) -> bool:
        if ((self.is_white and start.x == 6 and end.x == 8) or
                ((not self.is_white) and start.x == 1 and end.x == 0)):
            return True
        return False
