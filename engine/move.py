from typing import Iterator
from dataclasses import dataclass
from pieces import Piece, Pawn


@dataclass(frozen=True)
class Move:
    """
    An immutable class used to represent a Move in Chess.

    Attributes:
        piece (Piece or None): The instance of the Piece class that has been moved. Is None if no Piece was moved.

        start_position (tuple[int, int]): A tuple representing the start position of a piece's move on the board.
        It contains two integers: the x-coordinate (row index) and the y-coordinate (column index).

        end_position (tuple[int, int]): A tuple representing the end position of a piece's move on the board.
        It contains two integers: the x-coordinate (row index) and the y-coordinate (column index).
    """
    piece: Piece or None
    start_position: tuple[int, int]
    end_position: tuple[int, int]
    is_capture: bool = False
    is_king_side_castle: bool = False
    is_queen_side_castle: bool = False
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False
    promotion: Piece or None = None

    def __iter__(self) -> Iterator[Piece | None | tuple[int, int]]:
        """
        Allows instances to be unpacked into piece, start position, and end position.
        """
        yield self.piece
        yield self.start_position
        yield self.end_position

    def __repr__(self):
        move_str = ""
        # Handle castling moves first
        if self.is_king_side_castle:
            move_str += "0-0"
        elif self.is_queen_side_castle:
            move_str += "0-0-0"
        else:
            # convert to chessboard representation
            start_pos_str = chr(self.start_position[0] + 97) + str(8 - self.start_position[1])
            end_pos_str = chr(self.end_position[0] + 97) + str(8 - self.end_position[1])

            # Capture representation
            capture_str = 'x' if self.is_capture else ''

            if isinstance(self.piece, Pawn):
                move_str += f"{start_pos_str[0]}{capture_str}{end_pos_str}" if self.is_capture else end_pos_str
            else:
                piece_str = self.piece.symbol.upper() if self.piece else ''
                move_str += f"{piece_str}{capture_str}{end_pos_str}"

            # Handle promotions
            if self.promotion:
                move_str += f"={self.promotion.symbol.upper()}"

        # Handle check and checkmate
        if self.is_checkmate:
            move_str += "#"
        elif self.is_check:
            move_str += "+"

        # Handle stalemate
        if self.is_stalemate:
            move_str += "(stalemate)"

        return move_str

