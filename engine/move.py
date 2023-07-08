from typing import Iterator
from dataclasses import dataclass
from pieces import Piece


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

    def __iter__(self) -> Iterator[Piece | None | tuple[int, int]]:
        """
        Allows instances to be unpacked into piece, start position, and end position.
        """
        yield self.piece
        yield self.start_position
        yield self.end_position
