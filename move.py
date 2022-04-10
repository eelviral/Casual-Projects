from player import Player
from spot import Spot
from piece import Piece


class Move:
    """A class used to represent a Move being made on a chessboard

    Attributes
    ----------
    _player : Player
        The Player currently allowed to move
    _start : Spot
        Start position of a move
    _end : Spot
        End position of a move
    _piece_moved : Piece
        The Piece that is moving from start to end
    """

    def __init__(self, player, start, end):
        self._player = player
        self._start = start
        self._end = end
        self._piece_moved = start.piece
        self._piece_captured = None
        self._castling_move = False
        self._promotion_move = False
        self._en_passant_legal = False

    @property
    def player(self) -> Player:
        """Get the current player

        Returns: Player
        """
        return self._start

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
    def piece_captured(self) -> Piece:
        """Get or set captured piece

        Returns: Piece
        """
        return self._piece_captured

    @piece_captured.setter
    def piece_captured(self, value) -> None:
        if isinstance(value, Piece):
            self._piece_captured = value
        else:
            raise TypeError("piece_captured must be a Piece")

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
    def promotion_move(self):
        """Get or set pawn promotion move status

        Returns: bool
            - True if promotion move was played
            - False if promotion move was not played
        """
        return self._promotion_move

    @promotion_move.setter
    def promotion_move(self, value):
        if type(value) == bool:
            self._promotion_move = value
        else:
            raise TypeError("promotion_move must be a boolean")

    @property
    def en_passant_legal(self):
        """Get or set if en passant is currently legal

        Returns: bool
            - True if en passant is a legal move
            - False if en passant is an illegal move
        """
        return self._en_passant_legal

    @en_passant_legal.setter
    def en_passant_legal(self, value):
        if type(value) == bool:
            self._en_passant_legal = value
        else:
            raise TypeError("en_passant_legal must be a boolean")

    def __str__(self):
        string = f'{self._piece_moved} at ({self._start.x},{self._start.y})'
        if self._piece_captured is not None:
            return string + f' captured {self._piece_captured} at ({self._end.x},{self._end.y})'

        if self._promotion_move:
            return string + f'\n{self._piece_moved} promoted!'

        if self._castling_move:
            if self._piece_moved.is_white:
                return string + f'White {self._piece_moved} castled'
            else:
                return string + f'Black {self._piece_moved} castled'

        return string + f' moved to ({self._end.x},{self._end.y})'
