from piece import Piece, override
from itertools import product


class King(Piece):
    def __init__(self, white):
        super().__init__(white)
        self._in_check = False
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

        # Can't move if it will put king under attack
        if self.risk_check(board, end):
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

    @override(Piece)
    def controlled_squares(self, board, x, y) -> list:
        squares = []
        current_spot = board.get_box(x, y)
        for vector in product((0, -1, 1), (0, -1, 1)):
            next_x = x + vector[0]
            next_y = y + vector[1]
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

    def is_valid_castle(self, board, start, end) -> bool:
        if self.moves_made > 0:
            return False

        x = abs(end.x - start.x)
        y = end.y - start.y
        if abs(y) == 2 and x == 0:
            y_vector = -1 if y < 0 else 1
            for vector in range(y_vector, 2 * y_vector, y_vector):
                next_y = start.y + vector
                if self.risk_check(board, start.x, next_y):
                    return False

            from .rook import Rook
            rook_box = board.get_box(start.x, 0 if y < 0 else 7).piece
            if isinstance(rook_box, Rook) and rook_box.moves_made == 0:
                self.is_castling = True
                return True
        return False

    def risk_check(self, board, x, y) -> bool:
        for row in board.boxes:
            for box in row:
                if box.piece is None:
                    continue
                if (box.piece.is_white != self.is_white and
                        (x, y) in box.controlled_squares):
                    return True
        return False

    @property
    def in_check(self) -> bool:
        """Get or set if king is in check

        Returns: bool
            - True if king is in check
            - False if king is not in check
        """
        return self._in_check

    @in_check.setter
    def in_check(self, value):
        if type(value) == bool:
            self._in_check = value
        else:
            raise TypeError("in_check must be a boolean")

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
