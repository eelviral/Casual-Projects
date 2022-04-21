from piece import Piece
from itertools import product


class Knight(Piece):
    def __init__(self, white):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        """
        Determines if knight can currently move to marked position
        """
        x = abs(start.x - end.x)
        y = abs(start.y - end.y)

        # Don't move if same square
        if x == 0 and y == 0:
            return False

        if x * y == 2:
            # If end position is empty, move
            if end.piece is None:
                return True
            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                return True
        return False

    def controlled_squares(self, board, x, y) -> list:
        squares = []
        knight_moves = list(product((-2, 2), (-1, 1))) + list(product((-1, 1), (-2, 2)))
        for vector in knight_moves:
            next_x = x + vector[0]
            next_y = y + vector[1]
            if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                continue
            squares.append((next_x, next_y))
        return squares
