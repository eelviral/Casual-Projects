from pieces.piece import Piece, override
import math

class Knight(Piece):
    def __init__(self, white):
        super().__init__(white)       
    
    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        '''
        Determines if knight can currently move to marked position
        '''
        # Cannot move if there's a piece at the end position of the same color
        if end.get_piece().is_white() == self.is_white():
            return False
        
        x = math.abs(start.get_x() - end.get_x())
        y = math.abs(start.get_y() - end.get_y())
        
        return x * y == 2