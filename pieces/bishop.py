from piece import Piece, override


class Bishop(Piece):
    def __init__(self, white):
        super().__init__(white)

    @override(Piece)
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
                elif board.get_box(xi, yi).piece != None:
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
