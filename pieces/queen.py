from piece import Piece
from .rook import Rook
from .bishop import Bishop


class Queen(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.rook = Rook(white)
        self.bishop = Bishop(white)

    def can_move(self, board, start, end) -> bool:
        """
        Determines if queen can currently move to marked position
        """
        if (self.rook.can_move(board, start, end)
                or self.bishop.can_move(board, start, end)):
            return True
        return False

    def controlled_squares(self, board, x, y) -> list:
        rook_squares = self.rook.controlled_squares(board, x, y)
        bishop_squares = self.bishop.controlled_squares(board, x, y)
        return rook_squares + bishop_squares
