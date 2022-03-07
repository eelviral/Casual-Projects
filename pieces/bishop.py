import pieces
from pieces.piece import Piece

class Bishop(Piece):
    def __init__(self):
        super().__init__()
        print("Bishop " + self.piece)
