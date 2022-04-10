from piece import Piece, override


class Pawn(Piece):
    def __init__(self, white):
        super().__init__(white)
        self._is_promoted = False
        self._two_step_move = False
        self._moves_made = 0
        self._en_passant = False

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

        if self._moves_made == 0 and y == 0:
            if ((self.is_white and x == 2 and start.x == 1) or
                    ((not self.is_white) and x == -2 and start.x == 6)):
                self._two_step_move = True
                self._moves_made += 1
                return True
            else:
                self._moves_made += 1

        if not ((self.is_white and x == 1) or
                (not self.is_white) and x == -1):
            return False

        if y == 0:
            # If end position is empty, move
            if end.piece is None:
                self._moves_made += 1
                return True
            else:
                return False
        elif abs(x) == 1 and y == 1:
            if end.piece is None:
                # Check for en passant, and return False otherwise
                return self.is_valid_en_passant(board, start, end)

            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                self._moves_made += 1
                return True
        return self.is_valid_promotion(start, end)

    @override(Piece)
    def controlled_squares(self, board, x, y) -> list:
        squares = []
        current_spot = board.get_box(x, y)
        if self.is_white:
            x_vector = 1
        else:
            x_vector = -1

        next_x = x + x_vector
        for y_vector in [-1, 1]:
            next_y = y + y_vector
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue

            next_spot = board.get_box(next_x, next_y)
            if next_spot.piece is None:
                squares.append((next_x, next_y))
            else:
                if next_spot.piece.is_white != current_spot.piece.is_white:
                    squares.append((next_x, next_y))
                continue
        return squares

    def is_valid_promotion(self, start, end) -> bool:
        if ((self.is_white and start.x == 6 and end.x == 8) or
                ((not self.is_white) and start.x == 1 and end.x == 0)):
            return True
        return False

    def is_valid_en_passant(self, board, start, end) -> bool:
        x = end.x - start.x
        en_passant_piece = board.get_box(end.x - x, end.y).piece
        if (en_passant_piece is not None and
                en_passant_piece.two_step_move and
                en_passant_piece.moves_made == 1 and
                en_passant_piece.is_white != self.is_white):
            self._en_passant = True
            return True
        # Cannot "capture" an empty spot
        else:
            return False

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
    def two_step_move(self) -> bool:
        """Get or set pawn's two step move status

        Returns: bool
            - True if pawn made a two step move
            - False if pawn did not make a two step move
        """
        return self._two_step_move

    @two_step_move.setter
    def two_step_move(self, value) -> None:
        if type(value) == bool:
            self._two_step_move = value
        else:
            raise TypeError("two_step_move must be a boolean")

    @property
    def moves_made(self) -> int:
        """Get or set the amount of moves made by pawn

        Returns: int
        """
        return self._moves_made

    @moves_made.setter
    def moves_made(self, value) -> None:
        if isinstance(value, int):
            self._moves_made = value
        else:
            raise TypeError("moves_made must be an integer")

    @property
    def en_passant(self) -> bool:
        """Get or set en passant status

        Returns: bool
            - True if en passant was played
            - False if en passant was not played
        """
        return self._en_passant

    @en_passant.setter
    def en_passant(self, value) -> None:
        if type(value) == bool:
            self._en_passant = value
        else:
            raise TypeError("en_passant must be a boolean")
