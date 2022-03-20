from spot import Spot
from player import Player
from piece import Piece

class Move:
    castling_move = False
    
    def __init__(self, player, start, end):
        self.player = player
        self.start = start
        self.end = end
        self.piece_moved = start.get_piece()
        
    def is_castling_move(self) -> bool:
        return self.castling_move
    
    def set_castling_move(self, castling_move) -> None:
        self.castling_move = castling_move