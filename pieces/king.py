from piece import Piece
from itertools import product


class King(Piece):
    def __init__(self, white):
        super().__init__(white)
        self._in_check = False
        self._is_castling = False

    def can_move(self, board, start, end) -> bool:
        """
        Determines if king can currently move to marked position
        """

        x = abs(end.x - start.x)
        y = abs(end.y - start.y)
        self.is_castling = False

        # Don't move if same square
        if x == 0 and y == 0:
            return False

        # Can't move if it will put king in check
        if self.risk_check(board, end.x, end.y):
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

    def controlled_squares(self, board, x, y) -> list:
        squares = []
        for vector in product((0, -1, 1), (0, -1, 1)):
            next_x = x + vector[0]
            next_y = y + vector[1]
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue
            squares.append((next_x, next_y))
        return squares

    def legal_moves(self, board, x, y) -> list:
        moves = []
        current_spot = board.get_box(x, y)
        for vector in product((0, -1, 1), (0, -1, 1)):
            next_x = x + vector[0]
            next_y = y + vector[1]
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue

            next_spot = board.get_box(next_x, next_y)
            if next_spot.piece is None:
                if not self.risk_check(board, next_x, next_y):
                    moves.append((next_x, next_y))
            else:
                if (next_spot.piece.is_white != current_spot.piece.is_white and
                        not self.risk_check(board, next_x, next_y)):
                    moves.append((next_x, next_y))
                continue

        for vector in [-2, 2]:
            next_y = y + vector
            if next_y < 0 or next_y > 7:
                continue

            next_spot = board.get_box(x, next_y)
            if self.is_valid_castle(board, current_spot, next_spot):
                moves.append((x, next_y))
        return moves

    def is_valid_castle(self, board, start, end) -> bool:
        if self.moves_made > 0:
            return False

        if self.risk_check(board, start.x, start.y):
            return False

        x = abs(end.x - start.x)
        y = end.y - start.y
        if abs(y) == 2 and x == 0:
            y_vector = -1 if y < 0 else 1
            for vector in range(y_vector, 2 * y_vector, y_vector):
                next_y = start.y + vector
                if self.risk_check(board, start.x, next_y):
                    return False

                next_spot = board.get_box(start.x, next_y)
                if next_spot.piece is not None:
                    return False

            from .rook import Rook
            rook_box = board.get_box(start.x, 0 if y < 0 else 7)
            if isinstance(rook_box.piece, Rook) and rook_box.piece.moves_made == 0:
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
