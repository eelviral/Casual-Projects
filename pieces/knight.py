from piece import Piece, override


class Knight(Piece):
    def __init__(self, white):
        super().__init__(white)

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if knight can currently move to marked position
        """
        x = abs(start.x - end.x)
        y = abs(start.y - end.y)
        if x * y == 2:
            # If end position is empty, move
            if end.piece is None:
                return True
            # Cannot move if there's a piece at the end position of the same color
            if end.piece.is_white == self.is_white:
                return False
            else:
                return True
