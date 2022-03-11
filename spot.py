from pieces.piece import Piece

class Spot:
    def __init__(self, x, y, piece):
        self.set_piece(piece)
        self.set_pos_x(x)
        self.set_pos_y(y)
        
    def get_piece(self) -> Piece:
        return self.piece
    
    def set_piece(self, p):
        self.piece = p
    
    def get_pos_x(self) -> int:
        return self.x
    
    def set_pos_x(self, x):
        self.x = x
    
    def get_pos_y(self) -> int:
        return self.y
    
    def set_pos_y(self, y):
        self.y = y