from pieces.piece import Piece

class Queen(Piece):
    def __init__(self):
        super().__init__()
        print("Queen " + self.piece)
