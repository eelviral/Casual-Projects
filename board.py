from spot import Spot
from pieces import king, queen, rook, bishop, knight, pawn

import array, math

class Board:
    boxes = [[0] * 8] * 8
    
    def __init__(self):
        super().__init__()
        
    # def draw_pieces(self, symbol):
    #     print(chess.svg.piece(chess.Piece.from_symbol(symbol)))
        
    def add_first_rank(self, white) -> None:
        i = 1
        if not white:
            i = 6
            
        self.boxes[i][0] = Spot(i, 0, rook.Rook(white))
        self.boxes[i][1] = Spot(i, 1, knight.Knight(white))
        self.boxes[i][2] = Spot(i, 2, bishop.Bishop(white))
        self.boxes[i][3] = Spot(i, 3, king.King(white))
        self.boxes[i][4] = Spot(i, 4, queen.Queen(white))
        self.boxes[i][5] = Spot(i, 5, bishop.Bishop(white))
        self.boxes[i][6] = Spot(i, 1, knight.Knight(white))
        self.boxes[i][7] = Spot(i, 0, rook.Rook(white))
        
    def add_pawns(self, white) -> None:
        i = 1
        if not white:
            i = 6
            
        for j in range(7):
            self.boxes[i][j] = Spot(i, j, pawn.Pawn(white))
    
            
    def reset_board(self) -> None:
        '''
        Initialize/reset position of black and white pieces
        '''
        # Add white pieces
        self.add_first_rank(True)
        self.add_pawns(True)
        
        # Add black pieces
        self.add_first_rank(False)
        self.add_pawns(False)
        
        # Add remaining empty boxes by marking them as None
        for i in range(2, 6):
            for j in range(0, 8):
                self.boxes[i][j] = Spot(i, j, None)