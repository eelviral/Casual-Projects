from spot import Spot
from pieces import king, queen, rook, bishop, knight, pawn

import array, math

class Board:
    boxes = []
    
    def __init__(self):
        super().__init__()
        
    # def draw_pieces(self, symbol):
    #     print(chess.svg.piece(chess.Piece.from_symbol(symbol)))
        
    def add_first_rank(self, white) -> None:
        i = 0
        if not white:
            i = 7
            
        row = []
        row.append(Spot(i, 0, rook.Rook(white)))
        row.append(Spot(i, 1, knight.Knight(white)))
        row.append(Spot(i, 2, bishop.Bishop(white)))
        row.append(Spot(i, 3, king.King(white)))
        row.append(Spot(i, 4, queen.Queen(white)))
        row.append(Spot(i, 5, bishop.Bishop(white)))
        row.append(Spot(i, 6, knight.Knight(white)))
        row.append(Spot(i, 7, rook.Rook(white)))
        
        self.boxes.append(row)
             
    def add_pawns(self, white) -> None:
        i = 1
        if not white:
            i = 6

        self.boxes.append([Spot(i, j, pawn.Pawn(white)) for j in range(8)])
            
    def reset_board(self) -> None:
        '''
        Initialize/reset position of black and white pieces
        '''
        # Add white pieces
        self.add_first_rank(True)
        self.add_pawns(True)
        
        # Add empty boxes by marking them as None
        self.boxes.extend([[Spot(i, j, None) for j in range(0, 8)] for i in range(2, 6)])
        
        # Add black pieces
        self.add_pawns(False)
        self.add_first_rank(False)
        
    def __str__(self):
        return str([[str(piece) for piece in box] for box in self.boxes])