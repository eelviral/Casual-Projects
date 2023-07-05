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
        white_legal_moves (list[tuple[Piece, list[tuple[int, int]]]]): list of all white's legal moves
        black_legal_moves (list[tuple[Piece, list[tuple[int, int]]]]): list of all black's legal moves
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a given Board object.

        Args:
            board (Board): A Board object representing the current state of the chess board.
        """
        self._white_targets = {}
        self._black_targets = {}
        self._board = board
        self._last_move = Move(None, (-1, -1), (-1, -1), None)  # Initialize with an empty move

        self._white_legal_moves = {}
        self._black_legal_moves = {}
        self._checking_for_check = True
        self.update_legal_moves_and_targets()

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
        captured_piece = None  # Initialize with no captured piece

        if other_piece is not None and piece.can_capture_or_occupy_square(x=new_x, y=new_y, board=self.board):
            captured_piece = other_piece  # Capture the piece
            self.board.remove(other_piece)

        # Handle special moves
        self.handle_en_passant_capture(piece, new_x, new_y)
        self.handle_castle_move(piece, new_x, new_y)

        # Keep track of this move
        self.last_move = Move(piece, start_position=(piece.x, piece.y), end_position=(new_x, new_y), captured_piece=captured_piece)

        # Move the piece
        piece.x = new_x
        piece.y = new_y
        piece.has_moved = True
        self.update_legal_moves_and_targets()

    def undo_move(self):
        """
        Undo the last move.
        """
        # Store the last move temporarily
        temp_last_move = self._last_move

        # Undo the move
        piece_moved = self._last_move.piece
        piece_moved.x, piece_moved.y = self._last_move.start_position  # Move piece back to start position
        piece_moved.has_moved = False  # Reset moved status

        # Undo castling if it was the last move
        if isinstance(piece_moved, King) and abs(piece_moved.x - self._last_move.end_position[0]) == 2:
            if self._last_move.end_position[0] == 2:  # queen-side castle
                rook = self.board.piece_at(x=3, y=piece_moved.y)
                rook.x = 0
            else:  # king-side castle
                rook = self.board.piece_at(x=5, y=piece_moved.y)
                rook.x = 7
            rook.has_moved = False  # Reset moved status

        # Undo capture move
        if self._last_move.captured_piece:
            self._board.add(self._last_move.captured_piece)

        # Reset last move
        self._last_move = Move(None, (-1, -1), (-1, -1), None)  # Reset last move

        # If the last move was an en passant, restore the last move
        if isinstance(temp_last_move.piece, Pawn) and abs(temp_last_move.start_position[1] - temp_last_move.end_position[1]) == 2:
            self._last_move = temp_last_move

        self.update_legal_moves_and_targets()

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
                # self.undo_move()

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

    def calculate_moves_and_squares_for_piece(self, piece: Piece) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        """
        Calculate the legal moves and controlled squares for a given piece and return them as lists of tuples.

        Args:
            piece (Piece): The piece to calculate for.

        Returns:
            tuple: A tuple containing two lists of tuples where each tuple contains integer coordinates (x, y).
                The first list contains the legal moves and the second contains the controlled squares.
        """

        legal_moves = []
        controlled_squares = []

        for i in range(8):
            for j in range(8):
                if piece.legal_move(px=piece.x, py=piece.y, x=i, y=j, game_state=self):
                    legal_moves.append((i, j))
                if piece.is_controlled_square(current_x=piece.x, current_y=piece.y, target_x=i, target_y=j, game_state=self):
                    controlled_squares.append((i, j))

        return legal_moves, controlled_squares

    def update_legal_moves_and_targets(self):
        self._checking_for_check = False
        self._white_legal_moves = {}
        self._black_legal_moves = {}
        self._white_targets = {}
        self._black_targets = {}

        for piece in self.board.pieces:
            legal_moves, controlled_squares = self.calculate_moves_and_squares_for_piece(piece)
            if piece.is_white:
                self._white_legal_moves[piece.id] = legal_moves
                self._white_targets[piece.id] = controlled_squares
            else:
                self._black_legal_moves[piece.id] = legal_moves
                self._black_targets[piece.id] = controlled_squares

        self._checking_for_check = True

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

    @property
    def black_legal_moves(self) -> dict[Piece, list[tuple[int, int]]]:
        return self._black_legal_moves

    @property
    def white_legal_moves(self) -> dict[Piece, list[tuple[int, int]]]:
        return self._white_legal_moves

    @property
    def checking_for_check(self):
        return self._checking_for_check

    @property
    def black_targets(self) -> dict[Piece, list[tuple[int, int]]]:
        return self._black_targets

    @property
    def white_targets(self) -> dict[Piece, list[tuple[int, int]]]:
        return self._white_targets
