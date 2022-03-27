from piece import Piece, override


class Queen(Piece):
    def __init__(self, white):
        super().__init__(white)

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if queen can currently move to marked position
        """
        # If end position is empty, move
        if end.piece is None:
            return True

        # Cannot move if there's a piece at the end position of the same color
        if end.piece.is_white == self.is_white:
            return False
