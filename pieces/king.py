from pieces.piece import Piece
# from piece import Piece
class King(Piece):
    def __init__(self):
        super().__init__()
        print("King " + self.piece)