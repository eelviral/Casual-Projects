from piece import Piece, override


class Rook(Piece):
    def __init__(self, white):
        super().__init__(white)

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if rook can currently move to marked position
        """
        x = end.x - start.x
        y = end.y - start.y

        # Don't move if same square
        if x == 0 and y == 0:
            return False
        
        # If rook is moving horizontally or vertically
        if bool(x == 0) ^ bool(y == 0):
            # Make sure rook is not "jumping over" another piece horizontally
            if x == 0:
                y_vector = -1 if y < 0 else 1

                for i in range(1, 7):
                    yi = start.y + (y_vector * i)
                    if yi < 0 or yi > 7:
                        break
                    elif yi == end.y:
                        break
                    elif board.get_box(start.x, yi).piece is not None:
                        return False
            # Make sure rook is not "jumping over" another piece vertically
            elif y == 0:
                x_vector = -1 if x < 0 else 1

                for i in range(1, 7):
                    xi = start.x + (x_vector * i)
                    if xi < 0 or xi > 7:
                        break
                    elif xi == end.x:
                        break
                    elif board.get_box(xi, start.y).piece is not None:
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

    @override(Piece)
    def controlled_squares(self, board, x, y) -> list:
        squares = []
        current_spot = board.get_box(x, y)
        for i in [-1, 1]:
            for j in range(i, 7 * i, i):
                next_y = y + j
                if next_y < 0 or next_y > 7:
                    break

                next_spot = board.get_box(x, next_y)
                if next_spot.piece is None:
                    squares.append((x, next_y))
                else:
                    if next_spot.piece.is_white != current_spot.piece.is_white:
                        squares.append((x, next_y))
                    break

            for j in range(i, 7 * i, i):
                next_x = x + j
                if next_x < 0 or next_x > 7:
                    break

                next_spot = board.get_box(next_x, y)
                if next_spot.piece is None:
                    squares.append((next_x, y))
                else:
                    if next_spot.piece.is_white != current_spot.piece.is_white:
                        squares.append((next_x, y))
                    break
        return squares
