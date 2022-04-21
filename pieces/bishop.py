from piece import Piece
from .king import King
from itertools import product


class Bishop(Piece):
    def __init__(self, white):
        super().__init__(white)

    def can_move(self, board, start, end) -> bool:
        """
        Determines if bishop can currently move to marked position
        """
        try:
            x = end.x - start.x
            y = end.y - start.y
            slope = abs(y / x)
        except ZeroDivisionError:
            return False

        # Don't move if same square
        if x == 0 and y == 0:
            return False
        
        # If bishop is moving diagonally
        if slope == 1:
            x_vector = -1 if x < 0 else 1
            y_vector = -1 if y < 0 else 1

            # Make sure bishop is not "jumping over" another piece
            for i in range(1, 7):
                xi = start.x + (x_vector * i)
                yi = start.y + (y_vector * i)
                if (xi < 0 or xi > 7) or (yi < 0 or yi > 7):
                    break
                elif xi == end.x and yi == end.y:
                    break
                elif board.get_box(xi, yi).piece is not None:
                    return False

            # If end position is empty, move
            if end.piece is None:
                return True

            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                return True
        return False

    def controlled_squares(self, board, x, y):
        squares = []
        current_spot = board.get_box(x, y)
        for vector in product((-1, 1), (-1, 1)):
            i, j = vector[0], vector[1]
            for k in range(i, 7 * i, i):
                next_x = x + k
                next_y = y + j * k
                if (next_x < 0 or next_x > 7) or (next_y < 0 or next_y > 7):
                    break

                next_spot = board.get_box(next_x, next_y)
                if next_spot.piece is None:
                    squares.append((next_x, next_y))
                else:
                    if next_spot.piece.is_white != current_spot.piece.is_white:
                        if isinstance(next_spot.piece, King):
                            squares.append((next_x, next_y))
                            continue
                        else:
                            squares.append((next_x, next_y))
                    break
        return squares
