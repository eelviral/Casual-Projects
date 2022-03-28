from spot import Spot
from piece import Piece


class Move:
    """A class used to represent a Move being made on a chessboard

    Attributes
    ----------
    start : Spot
        Start position of a move
    end : Spot
        End position of a move
    piece_moved : Piece
        The Piece that is moving from start to end
    """
    _castling_move = False
    _promotion = False

    def __init__(self, start, end):
        # self.player = player
        self._start = start
        self._end = end
        self._piece_moved = start.piece

    @property
    def start(self) -> Spot:
        """Get start position Spot

        Returns: Spot
        """
        return self._start

    @property
    def end(self) -> Spot:
        """Get end position Spot

        Returns: Spot
        """
        return self._end

    @property
    def piece_moved(self) -> Piece:
        """Get the moving piece

        Returns: Piece
        """
        return self._piece_moved

    @property
    def castling_move(self) -> bool:
        """Get or set castling move status

        Returns: bool
            - True if castling move was played
            - False if castling move was not played
        """
        return self._castling_move

    @castling_move.setter
    def castling_move(self, value) -> None:
        if type(value) == bool:
            self._castling_move = value
        else:
            raise TypeError("is_castling_move must be a boolean")
    
    @property    
    def promotion(self):
        """Get or set pawn promotion status

        Returns: bool
            - True if a pawn is being promoted
            - False if no pawn is being promoted
        """
        return self._promotion

    @promotion.setter
    def promotion(self, value):
        if type(value) == bool:
            self._promotion = value
        else:
            raise TypeError("promotion must be a boolean")
        