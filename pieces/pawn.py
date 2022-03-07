from pieces.piece import Piece

class Pawn(Piece):
    def __init__(self):
        super().__init__()
        print("Pawn " + self.piece)