from dataclasses import dataclass
from pieces import Piece


@dataclass(frozen=True)
class Move:
    """
    A class used to represent a Move in Chess.

    Attributes:
        piece (Piece): The piece that has been moved.
        start_position (tuple[int, int]): The start position of the piece on the board.
        end_position (tuple[int, int]): The end position of the piece on the board.
    """
    piece: Piece
    start_position: tuple[int, int]
    end_position: tuple[int, int]
    
    def __iter__(self):
        yield self.piece
        yield self.start_position
        yield self.end_position
