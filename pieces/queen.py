from piece import Piece, override
from pieces.rook import Rook
from pieces.bishop import Bishop


class Queen(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.rook = Rook(white)
        self.bishop = Bishop(white)

    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        """
        Determines if queen can currently move to marked position
        """
        if (self.rook.can_move(board, start, end)
                or self.bishop.can_move(board, start, end)):
            return True
        return False
