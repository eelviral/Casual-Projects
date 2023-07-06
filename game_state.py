import copy
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
        # Do not proceed with non-legal moves
        if not piece.legal_move(px=piece.x, py=piece.y, x=new_x, y=new_y, game_state=self):
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

        self.last_move = Move(piece, start_position=(original_x, original_y), end_position=(new_x, new_y))
        piece.has_moved = True
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
        if isinstance(piece, King) and abs(new_x - piece.x) == 2:
            rook_x = 0 if new_x < piece.x else 7
            rook = self.board.piece_at(x=rook_x, y=new_y)
            if rook is not None and isinstance(rook, Rook):
                # Determine the new position for the rook and move it there
                rook_new_x = 3 if new_x < piece.x else 5
                rook.x = rook_new_x
                rook.has_moved = True

    def calculate_legal_moves_for_piece(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Calculate all legal moves for a given piece.

        Args:
            piece (Piece): The piece to calculate legal moves for.

        Returns:
            List[Tuple[int, int]]: List of legal moves, each move is represented by a tuple (x, y).
        """
        legal_moves = []

        # Generate all possible moves for the piece
        possible_moves = []
        for i in range(8):
            for j in range(8):
                # If the move is legal and either the king is not in check or the move protects the king
                if piece.legal_move(px=piece.x, py=piece.y, x=i, y=j, game_state=self):
                    possible_moves.append((i, j))
                    
        for x, y in possible_moves:
            # Create a temporary copy of the game state and make the move
            temp_state = self.copy()
            temp_piece = temp_state.board.piece_at(x=piece.x, y=piece.y)

            # If the move results in a successful move and doesn't cause a check, add it to the legal moves
            if temp_state.move_piece(piece=temp_piece, new_x=x, new_y=y) and not temp_state.is_in_check(piece.team):
                legal_moves.append((x, y))
                
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
            
    def is_in_check(self, team: TeamType):
        """
        Check if a king is in check.

        Args:
            team (TeamType): The team of the king to check.

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        king = self.get_king(team)

        # Check each enemy piece if they can reach the king's position
        for piece in self.board.pieces:
            if piece.team != team:
                if piece.is_controlled_square(piece.x, piece.y, king.x, king.y, self):
                    return True
        return False

    def move_protects_king(self, px: int, py: int, x: int, y: int) -> bool:
        """
        Checks if a proposed move would result in the current player's King being in check.

        The method creates a temporary copy of the game state, makes the proposed move in this copied game state, 
        and then checks if the resulting state would put the King in check. The real game state remains unaffected.

        Args:
            px (int): The current x-coordinate of the piece that is proposed to be moved.
            py (int): The current y-coordinate of the piece that is proposed to be moved.
            x (int): The proposed new x-coordinate for the piece.
            y (int): The proposed new y-coordinate for the piece.

        Returns:
            bool: True if the proposed move would not result in the King being in check, False otherwise.
        """
        temp_state = self.copy()
        temp_piece = temp_state.board.piece_at(x=px, y=py)
        temp_state.move_piece(piece=temp_piece, new_x=x, new_y=y)
        return not temp_state.is_in_check(temp_piece.team)

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
        
    def copy(self):
        """Creates a deep copy of the game state."""
        new_game_state = copy.deepcopy(self)
        return new_game_state

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
