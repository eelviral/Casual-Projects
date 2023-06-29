from dataclasses import replace
from board import Board
from pieces import Piece, King, Pawn
from move import Move
from pieces import Queen
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
        self._last_move = Move(None, (-1, -1), (-1, -1)) # Initialize with an empty move
    
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

        # If this move was an en passant capture, remove the captured piece
        if isinstance(self.last_move.piece, Pawn) and isinstance(piece, Pawn):
            if piece.en_passant(px=piece.x, py=piece.y, x=new_x, y=new_y, game_state=self):
                self.board.remove(self.last_move.piece)

        # Keep track of this move
        self.last_move = Move(piece, start_position=(piece.x, piece.y), end_position=(new_x, new_y))

        # Move the piece
        piece.x = new_x
        piece.y = new_y     

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
        
    def is_checkmate(self):
        # Get the current player
        current_player = self.get_current_player()

        # Get the opponent's pieces
        opponent_pieces = self.get_opponent_pieces()

        # Get the current player's king
        king = self.get_king(current_player)

        # Check if the king is in check
        if not king.is_in_check(opponent_pieces):
            return False

        # Check if the king has any safe squares to move to
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x = king.x + dx
                new_y = king.y + dy
                if self.board.is_valid_position(new_x, new_y):
                    if not self.board.is_square_under_attack(new_x, new_y, opponent_pieces):
                        return False

        # Check if any of the current player's pieces can block the check
        for piece in self.get_current_player_pieces():
            if isinstance(piece, King):
                continue
            if piece.can_block_check(king, opponent_pieces):
                return False

        # If none of the conditions are met, it's a checkmate
        return True
    
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
    
    def get_current_player(self):
        pass
    
    def get_opponent_pieces(self):
        pass
    
    def get_king(self):
        pass
    
    def get_current_player_pieces(self):
        pass
    
    def is_promotion(self):
        """
        Checks if a pawn is eligible for promotion.

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
        self.board.remove(piece)
        new_piece = promotion_piece(x=piece.x, y=piece.y, team=piece.team, is_white=piece.is_white)
        self.board.add(new_piece)
