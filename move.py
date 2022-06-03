from player import Player
from spot import Spot
from piece import Piece
from board import Board


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
        The Piece that moved
    _piece_captured : Piece
        The Piece that was captured
    _castling_move : bool
        If castling move was played
    _promotion_move : bool
        If promotion is supposed to occur
    _en_passant_legal : bool
        If this move makes en passant legal for the next move
    _en_passant_move : bool
        If en passant move was played
    _previous_board : Board
        The board state before this move was played
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
        self._en_passant_move = False
        self._previous_board = None

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
        """Get or set if castling move was made

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

    @property
    def en_passant_move(self):
        """Get or set if en passant was played

        Returns: bool
            - True if en passant was played
            - False if en passant was not played
        """
        return self._en_passant_move

    @en_passant_move.setter
    def en_passant_move(self, value):
        if type(value) == bool:
            self._en_passant_move = value
        else:
            raise TypeError("en_passant_legal must be a boolean")

    @property
    def previous_board(self) -> Board:
        """Get or set the previous board

        :return: Board
        """
        return self._previous_board

    @previous_board.setter
    def previous_board(self, value):
        if isinstance(value, Board):
            self._previous_board = value
        else:
            raise TypeError("previous_board must be a Board")

    def __repr__(self):
        string = f'{repr(self.piece_moved)} at ({self.start.x},{self.start.y})'
        if self.piece_captured is not None:
            if self.en_passant_move:
                x = self.end.x - self.start.x
                string += f' captured {repr(self.piece_captured)} at ({self.end.x - x},{self.end.y}) and'
            else:
                return string + f' captured {repr(self.piece_captured)} at ({self.end.x},{self.end.y})'

        if self._promotion_move:
            return string + f'\n{repr(self.piece_moved)} promoted!'

        if self._castling_move:
            y = self.end.y - self.start.y
            return string + f" castled {'king' if y < 0 else 'queen'} side"

        return string + f' moved to ({self.end.x},{self.end.y})'
