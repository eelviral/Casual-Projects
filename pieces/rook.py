from pieces.piece import Piece

class Rook(Piece):
    def __init__(self):
        super().__init__()
        print("Rook " + self.piece)