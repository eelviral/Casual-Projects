from pieces.piece import Piece, override

class Pawn(Piece):
    def __init__(self, white):
        super().__init__(white)       
    
    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        '''
        Determines if pawn can currently move to marked position
        '''
        # Cannot move if there's a piece at the end position of the same color
        if end.get_piece().is_white() == self.is_white():
            return False