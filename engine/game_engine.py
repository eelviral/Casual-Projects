from dataclasses import replace
from pieces import Piece, Pawn, King, Rook
from utils import TeamType
from engine.move import Move
from engine.game_event import GameEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import ChessGame


class GameEngine:
    """
    A class to represent a game engine for chess. This engine handles game moves and
     interactions between pieces on the board.

    Attributes:
        game (ChessGame): A ChessGame object representing the chess game.
        board (Board): A Board object representing the current chess board.
        last_move (Move): A Move object used to represent the last move played on the board.
    """

    def __init__(self, chess_game: 'ChessGame'):
        """
        Constructs a new game engine with the given chess game.

        Args:
            chess_game (ChessGame): The chess game being played.
        """
        self.game = chess_game
        self.board = chess_game.board
        self._last_move = Move(None, (-1, -1), (-1, -1))  # Initialize with an empty move

    @property
    def last_move(self) -> Move:
        """
        Provides the last move that was made on the chess board. This can be useful for undo operations,
        logging, and implementing certain game rules.

        Returns:
            Move: A Move object representing the last move.
        """
        return self._last_move

    @last_move.setter
    def last_move(self, move: Move):
        """
        Sets the last move that was made on the chess board. This should be updated every time a move
        is made.

        Args:
            move (Move): A Move object representing the last move.
        """
        self._last_move = replace(move)

    def move_piece(self, piece: Piece, new_x: int, new_y: int) -> bool:
        """
        Moves a piece to a new position on the board. If the new position is occupied by another piece,
        that piece is removed from the board. If the new position is occupied by an ally, the move is not made.

        Args:
            piece (Piece): The piece to move.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        Returns:
            bool: True if the move is successful, False otherwise.
        """
        self.game.event = None  # reset game event

        # Do not proceed with non-legal moves
        if not piece.legal_move(px=piece.x, py=piece.y, x=new_x, y=new_y, chess_game=self.game):
            return False

        # Check if there's a piece at the new position
        other_piece = self.board.piece_at(x=new_x, y=new_y)

        # Handle special moves
        self.handle_en_passant_capture(piece, new_x, new_y)
        self.handle_castle_move(piece, new_x, new_y)

        # Attempt the move and store the original position
        original_x, original_y = piece.x, piece.y
        piece.x, piece.y = new_x, new_y

        # Move is legal, so finalize it
        if other_piece is not None and piece.can_capture_or_occupy_square(x=original_x, y=original_y, board=self.board):
            self.board.remove(other_piece)
            self.game.event = GameEvent.CAPTURE

        self.last_move = Move(piece, start_position=(original_x, original_y), end_position=(new_x, new_y))
        piece.has_moved = True
        self.game.status.positions.append(self.board.fen())
        return True

    def handle_en_passant_capture(self, piece: Piece, new_x: int, new_y: int):
        """
        Handles the special chess move "en passant".
        If the conditions for en passant are met, this function removes the opponent's last-moved pawn

        Args:
            piece (Piece): The pawn that is capturing the opponent's pawn "en passant".
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        """
        if isinstance(self.last_move.piece, Pawn) and isinstance(piece, Pawn):
            if piece.en_passant(px=piece.x, py=piece.y, x=new_x, y=new_y, game_engine=self):
                self.board.remove(self.last_move.piece)
                self.game.event = GameEvent.CAPTURE

    def handle_castle_move(self, piece: Piece, new_x: int, new_y: int):
        """
        Handles the special chess move "castling".
        If the conditions for castling are met, this function moves the corresponding rook.

        Args:
            piece (Piece): The king that is castling.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        """
        if isinstance(piece, King) and abs(new_x - piece.x) == 2:
            rook_x = 0 if new_x < piece.x else 7
            rook = self.board.piece_at(x=rook_x, y=new_y)
            if rook is not None and isinstance(rook, Rook):
                # Determine the new position for the rook and move it there
                rook_new_x = 3 if new_x < piece.x else 5
                rook.x = rook_new_x
                rook.has_moved = True
                self.game.event = GameEvent.CASTLE

    def promote(self, piece: Pawn, promotion_piece: type[Piece]):
        """
        Promotes a pawn to a different piece.

        Args:
            piece (Pawn): The pawn to be promoted.
            promotion_piece (type[Piece]): The type of piece that the pawn should be promoted to.
        """
        self.board.remove(piece)
        new_piece = promotion_piece(x=piece.x, y=piece.y, team=piece.team, is_white=piece.is_white)
        self.board.add(new_piece)
