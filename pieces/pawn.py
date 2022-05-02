from piece import Piece


class Pawn(Piece):
    def __init__(self, white, at_top_of_board):
        super().__init__(white)
        self._is_promoted = False
        self._two_step_move = False
        self._moves_made = 0
        self._en_passant = False
        self.top_spawned = at_top_of_board

    def can_move(self, board, start, end) -> bool:
        """
        Determines if pawn can currently move to marked position
        """

        x = end.x - start.x
        y = abs(end.y - start.y)

        # Don't move if same square
        if x == 0 and y == 0:
            return False

        if self.moves_made == 0 and y == 0:
            if end.piece is not None:
                return False

            if ((self.top_spawned and x == 2 and start.x == 1) or
                    ((not self.top_spawned) and x == -2 and start.x == 6)):
                self.two_step_move = True
                return True

        if not ((self.top_spawned and x == 1) or
                (not self.top_spawned) and x == -1):
            return False

        if y == 0:
            # If end position is empty, move
            if end.piece is None:
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
                return True
        return self.is_valid_promotion(start, end)

    def controlled_squares(self, board, x, y) -> list:
        squares = []
        if self.top_spawned:
            x_vector = 1
        else:
            x_vector = -1

        next_x = x + x_vector
        for y_vector in [-1, 1]:
            next_y = y + y_vector
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue
            squares.append((next_x, next_y))
        return squares

    def legal_moves(self, board, x, y) -> list:
        moves = []
        current_spot = board.get_box(x, y)
        if self.top_spawned:
            x_vector = 1
        else:
            x_vector = -1

        if self.moves_made == 0:
            for i in range(x_vector, 2 * x_vector, x_vector):
                next_x = x + i
                if next_x < 0 or next_x > 7:
                    break
                next_spot = board.get_box(next_x, y)
                if next_spot.piece is None:
                    moves.append((next_x, y))
        else:
            next_x = x + x_vector
            if 0 <= next_x <= 7:
                next_spot = board.get_box(next_x, y)
                if next_spot.piece is None:
                    moves.append((next_x, y))

        next_x = x + x_vector
        for y_vector in [-1, 1]:
            next_y = y + y_vector
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue

            next_spot = board.get_box(next_x, next_y)
            if next_spot.piece is None:
                moves.append((next_x, next_y))
            else:
                if next_spot.piece.is_white != current_spot.piece.is_white:
                    moves.append((next_x, next_y))
                continue
        return moves

    def is_valid_promotion(self, start, end) -> bool:
        if ((self.top_spawned and start.x == 6 and end.x == 8) or
                ((not self.top_spawned) and start.x == 1 and end.x == 0)):
            return True
        return False

    def is_valid_en_passant(self, board, start, end) -> bool:
        x = end.x - start.x
        en_passant_piece = board.get_box(end.x - x, end.y).piece

        # Make sure that en passant only works on another pawn
        if not isinstance(en_passant_piece, Pawn):
            return False

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
