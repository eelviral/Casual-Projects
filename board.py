from dataclasses import replace
from type import TeamType
from pieces import *
from move import Move


class Board:
    """
    A class used to represent a Chess Board.

    Attributes:
        board (list): A list of Piece objects representing the current state of the chess board.
        last_move (Move): A Move object used to represent the last move played on the board.
    """

    def __init__(self):
        """
        Initializes a Board with an empty list and calls the method to initialize the board with pieces.
        """
        self.board = []
        self._initialize_board()
        
        self._last_move = Move(None, (-1, -1), (-1, -1)) # Initialize with an empty move
    
    def _initialize_board(self):
        """
        Initializes the board with chess pieces in their starting positions.
        The board is represented as a list of Piece objects.
        """
        # Add non-pawn pieces
        for p in range(2):
            team_type = TeamType.OPPONENT if p == 0 else TeamType.ALLY
            is_white = False if team_type == TeamType.OPPONENT else True
            y = 0 if team_type == TeamType.OPPONENT else 7

            self.board.append(Rook(x=0, y=y, team=team_type, is_white=is_white))
            self.board.append(Knight(x=1, y=y, team=team_type, is_white=is_white))
            self.board.append(Bishop(x=2, y=y, team=team_type, is_white=is_white))
            self.board.append(Queen(x=3, y=y, team=team_type, is_white=is_white))
            self.board.append(King(x=4, y=y, team=team_type, is_white=is_white))
            self.board.append(Bishop(x=5, y=y, team=team_type, is_white=is_white))
            self.board.append(Knight(x=6, y=y, team=team_type, is_white=is_white))
            self.board.append(Rook(x=7, y=y, team=team_type, is_white=is_white))

        # Add pawns
        for i in range(8):
            self.board.append(Pawn(x=i, y=1, team=TeamType.OPPONENT, is_white=False))
            self.board.append(Pawn(x=i, y=6, team=TeamType.ALLY, is_white=True))

    def piece_at(self, x: int, y: int) -> Piece or None:
        """
        Returns the piece at a given position on the board.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            Piece or None: The piece at the given position, or None if there is no piece.
        """
        for piece in self.board:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def move_piece(self, piece: Piece, new_x: int, new_y: int):
        """
        Moves a piece to a new position on the board. If the new position is occupied by another piece,
        that piece is removed from the board. If the new position is occupied by an ally, the move is not made.

        Args:
            piece (Piece): The piece to move.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
        """
        if not piece.legal_move(px=piece.x, py=piece.y, x=new_x, y=new_y, board=self):
            # If the move is not legal, do not proceed with the move
            return

        # Check if there's a piece at the new position
        for other_piece in self.board:
            if other_piece.x == new_x and other_piece.y == new_y:
                # If the piece at the new position is from the same team, do not move the piece
                if other_piece.team == piece.team:
                    return
                # If the piece at the new position is from the opposing team, remove it from the board
                else:
                    self.board.remove(other_piece)
                break
        
        # If this move was an en passant capture, remove the captured piece
        if isinstance(self.last_move.piece, Pawn) and isinstance(piece, Pawn):
            if piece._en_passant(px=piece.x, py=piece.y, x=new_x, y=new_y, board=self):
                self.board.remove(self.last_move.piece)

        # Keep track of this move
        self.last_move = Move(piece, start_position=(piece.x, piece.y), end_position=(new_x, new_y))
            
        # Move the piece
        piece.x = new_x
        piece.y = new_y
    
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
    
    
    def __getitem__(self, index):
        """
        Returns the Piece object at the given index in the board list.

        Args:
            index (int): The index of the piece in the board list.

        Returns:
            Piece: The Piece object at the given index.
        """
        return self.board[index]
