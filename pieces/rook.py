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
