from dataclasses import replace
from board import Board
from pieces import Piece, King, Pawn, Rook
from move import Move
from type import TeamType


class GameState:
    """
    A class used to represent the current state of a Chess game.

    Attributes:
        board (Board): A Board object representing the current state of the chess board.
        last_move (Move): A Move object used to represent the last move played on the board.
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a given Board object.

        Args:
            board (Board): A Board object representing the current state of the chess board.
        """
        self._board = board
        self._last_move = Move(None, (-1, -1), (-1, -1))  # Initialize with an empty move

    def move_piece(self, piece: Piece, new_x: int, new_y: int):
        """
        Moves a piece to a new position on the board. If the new position is occupied by another piece,
        that piece is removed from the board. If the new position is occupied by an ally, the move is not made.

        Args:
            piece (Piece): The piece to move.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        """
        # Do not proceed with non-legal moves
        if not piece.legal_move(px=piece.x, py=piece.y, x=new_x, y=new_y, game_state=self):
            return

        # Check if there's a piece at the new position
        other_piece = self.board.piece_at(x=new_x, y=new_y)
        if other_piece is not None and piece.can_capture_or_occupy_square(x=new_x, y=new_y, board=self.board):
            self.board.remove(other_piece)

        # Handle special moves
        self.handle_en_passant_capture(piece, new_x, new_y)
        self.handle_castle_move(piece, new_x, new_y)

        # Keep track of this move
        self.last_move = Move(piece, start_position=(piece.x, piece.y), end_position=(new_x, new_y))

        # Move the piece
        piece.x = new_x
        piece.y = new_y
        piece.has_moved = True

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
            if piece.en_passant(px=piece.x, py=piece.y, x=new_x, y=new_y, game_state=self):
                self.board.remove(self.last_move.piece)

    def handle_castle_move(self, piece: Piece, new_x: int, new_y: int):
        """
        Handles the special chess move "castling".
        If the conditions for castling are met, this function moves the corresponding rook.

        Args:
            piece (Piece): The king that is castling.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        """
        if isinstance(piece, King) and piece.can_castle(px=piece.x, py=piece.y, x=new_x, y=new_y, game_state=self):
            # Determine which rook to move (0 for queen-side, 7 for king-side)
            rook_x = 0 if new_x < piece.x else 7
            rook = self.board.piece_at(x=rook_x, y=new_y)
            if rook is not None and isinstance(rook, Rook):
                # Determine the new position for the rook and move it there
                rook.x = 3 if new_x < piece.x else 5
                rook.has_moved = True

    def calculate_legal_moves_for_piece(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Calculate the legal moves for a given piece and return them as a list of tuples.

        Args:
            piece (Piece): The piece to calculate legal moves for.

        Returns:
            list[tuple[int, int]]: List of tuples where each tuple contains integer coordinates (x, y).
        """
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if piece.legal_move(px=piece.x, py=piece.y, x=i, y=j, game_state=self):
                    legal_moves.append((i, j))
        return legal_moves

    def get_king(self, team: TeamType) -> King:
        """
        Returns the king piece of the given team.

        Args:
            team (TeamType): The team whose king to return.

        Returns:
            King: The king of the given team.
        """
        for piece in self.board.pieces:
            if isinstance(piece, King) and piece.team == team:
                return piece

    def is_promotion(self):
        """
        Checks if a pawn is eligible for promotion. A pawn is eligible for promotion if it reaches
        the opponent's end of the board.

        Returns:
            bool: True if a promotion is possible, False otherwise.
        """
        last_move = self.last_move

        # Check if the last move was made by a pawn
        if isinstance(last_move.piece, Pawn):
            x, y = last_move.end_position
            promotion_rank = 7 if last_move.piece.team == TeamType.OPPONENT else 0

            # Check if the pawn reached the promotion rank
            if y == promotion_rank:
                return True

        return False

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

    @property
    def board(self):
        """Gets the current state of the chess board.

        Returns:
            Board: A Board object representing the current chess board configuration.
        """
        return self._board

    @property
    def last_move(self):
        """
        Gets the last move on the chess board.

        Returns:
            Move: A Move object representing the last move.
        """
        return self._last_move

    @last_move.setter
    def last_move(self, move: Move):
        """
        Sets the last move on the chess board.

        Args:
            move (Move): A Move object representing the last move.
        """
        self._last_move = replace(move)
