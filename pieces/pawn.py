from pieces import Piece
from type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from game_state import GameState


class Pawn(Piece):
    """
    Represents a Pawn piece in a chess game. Inherits from the Piece class.
    
    The Pawn class is a subclass of the Piece class, with a specific type of PieceType.PAWN.
    
    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'P', 'p').
        type (PieceType): The type of the piece (PAWN).
    """

    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a Pawn with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'P' if is_white else 'p'
        super().__init__(x, y, team, is_white, symbol, PieceType.PAWN)

    def legal_move(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determine if a pawn's move is legal.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        if self._moving_forward(px, py, x, y, board=game_state.board) or \
                self._capturing(px, py, x, y, board=game_state.board) or \
                self.en_passant(px, py, x, y, game_state):
            return True
        else:
            return False

    def _moving_forward(self, px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Check if the pawn is moving forward.
        
        The pawn moves straight forward one square, with the option to move two squares 
        if it has not yet moved (pawn's first move). The pawn can't jump over pieces.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.

        Returns:
            bool: True if the pawn is moving forward correctly, False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        is_in_starting_position = (py == 6 if self.team == TeamType.ALLY else py == 1)
        return dx == 0 and (dy == direction or (is_in_starting_position and dy == 2 * direction)) and board.piece_at(x,
                                                                                                                     y) is None

    def _capturing(self, px: int, py: int, x: int, y: int, board: 'Board') -> bool:
        """
        Check if the pawn is capturing an opponent's piece.

        The pawn can capture an enemy piece on either of the two spaces adjacent to 
        the space in front of it (diagonal forward), but cannot move to these spaces 
        if they are vacant.

        Args:
            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            board (Board): The game board.

        Returns:
            bool: True if the pawn is capturing correctly, False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        return (abs(dx) == 1 and dy == direction) and \
            (board.piece_at(x, y) is not None and self.can_capture_or_occupy_square(x, y, board))

    def en_passant(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Check if the pawn is capturing by "en passant".

        En passant is a special pawn capture that can only occur immediately after a pawn 
        moves two ranks forward from its starting position. The opponent captures the 
        just-moved pawn "as it passes" through the first square.

        Args:

            px (int): The current x-coordinate of the pawn.
            py (int): The current y-coordinate of the pawn.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the pawn is capturing by "en passant", False otherwise.
        """
        dx = x - px
        dy = y - py
        direction = -1 if self.team == TeamType.ALLY else 1
        capture_rank = 3 if self.team == TeamType.ALLY else 4  # Decide the capture rank based on team

        last_move = game_state.last_move
        if last_move is None:
            return False

        last_piece_moved, last_start_pos, last_end_pos = last_move
        if not isinstance(last_piece_moved, Pawn):  # Last piece moved must be a Pawn
            return False

        # Make sure the pawn can't capture allies
        if self.is_white == last_piece_moved.is_white:
            return False

        is_on_same_row = last_end_pos[1] == py
        is_directly_next_to_pawn = abs(last_end_pos[0] - px) == 1

        # The pawn must be beside this pawn
        if is_on_same_row and is_directly_next_to_pawn:
            # The pawn must have moved 2 steps
            if last_start_pos[1] - last_end_pos[1] == 2 * direction:
                # This pawn must be moving diagonally forward in the correct direction
                if py == capture_rank and dy == direction and dx == (last_end_pos[0] - px):
                    return True

        return False
