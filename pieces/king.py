from piece import Piece, override
import math

class King(Piece):
    castled = False
    
    def __init__(self, white):
        super().__init__(white)    
    
    @override(Piece)
    def can_move(self, board, start, end) -> bool:
        '''
        Determines if king can currently move to marked position
        '''
        # Cannot move if there's a piece at the end position of the same color
        if end.get_piece().is_white() == self.is_white():
            return False
        
        x = math.abs(start.get_pos_x() - end.get_pos_x())
        y = math.abs(start.get_pos_y() - end.get_pos_y())
        
        if (x + y) == 1:
            return True
        
        return self.is_valid_castle(board, start, end)

    def is_castled(self) -> bool:
        return self.castled
    
    def set_castled(self, castled):
        self.castled = castled
        
    def is_valid_castle(self, board, start, end):
        if self.castled:
            return False

        
    def is_castle_move(self, start, end):
        pass