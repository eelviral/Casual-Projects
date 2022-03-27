from piece import Piece, override


class Knight(Piece):
    def __init__(self, white):
        super().__init__(white)

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if knight can currently move to marked position
        """
        # If end position is empty, move
        if end.piece is None:
            return True
        # Cannot move if there's a piece at the end position of the same color
        elif end.piece.is_white == self.is_white:
            return False

        x = abs(start.get_pos_x() - end.get_pos_x())
        y = abs(start.get_pos_y() - end.get_pos_y())

        return x * y == 2
