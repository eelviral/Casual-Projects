from pieces import Piece
from pieces.rook import Rook
from type import PieceType, TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_state import GameState


class King(Piece):
    """
    Represents a King piece in a chess game. Inherits from the Piece class.
    
    The King class is a subclass of the Piece class, with a specific type of PieceType.KING.
    
    Attributes:
        x (int): The x-coordinate of the piece on the board.
        y (int): The y-coordinate of the piece on the board.
        team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
        is_white (bool): The color of the piece (e.g. True if white, False if black).
        symbol (str): The character symbol representing the piece (e.g., 'K', 'k').
        type (PieceType): The type of the piece (KING).
        has_moved (bool): Determines whether the King has already moved (at least once) or not.
    """

    def __init__(self, x: int, y: int, team: TeamType, is_white: bool):
        """
        Initializes a King with a team, symbol, and coordinates.

        Args:
            x (int): The x-coordinate of the piece on the board.
            y (int): The y-coordinate of the piece on the board.
            team (TeamType): The team the piece belongs to (e.g., OPPONENT, ALLY).
            is_white (bool): The color of the piece (e.g. True if white, False if black).
        """
        symbol = 'K' if is_white else 'k'
        super().__init__(x, y, team, is_white, symbol, PieceType.KING)
        self.has_moved = False

    def legal_move(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determine if a King's move is legal.

        Args:
            px (int): The current x-coordinate of the King.
            py (int): The current y-coordinate of the King.
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        dx = abs(x - px)
        dy = abs(y - py)

        # Make sure the move doesn't place the king in check
        if game_state.checking_for_check and self.is_move_into_check(x, y, game_state):
            return False

        return self.can_castle(px, py, x, y, game_state) or \
            ((dx <= 1 and dy <= 1) and self.can_capture_or_occupy_square(x, y, board=game_state.board))

    def can_castle(self, px: int, py: int, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determines if a castling move is possible for the King.

        Castling is a special move in chess involving the King and one of the rooks of the same color.
        It is the only move that allows a player to move two pieces in the same move. Castling can only be done
        if the King has never moved, the Rook involved has never moved, the squares between them are not occupied,
        the King is not in check, and the King does not pass through or land on a square that is attacked by an enemy piece.

        Parameters:
            px (int): The current x-coordinate of the King.
            py (int): The current y-coordinate of the King.
            x (int): The x-coordinate of the proposed move.
            y (int): The y-coordinate of the proposed move.
            game_state (GameState): The current state of the game.

        Returns:
            bool: True if castling is allowed, False otherwise.
        """
        dx = abs(x - px)
        dy = abs(y - py)

        if dy == 0 and dx == 2:
            if self.has_moved or self.is_in_check(game_state):  # King cannot castle if it has moved or is in check
                return False

            direction = 1 if x > px else -1  # Determine which rook to check for (king-side or queen-side)

            for i in range(1, dx):
                # No pieces can be between the king and rook
                if game_state.board.piece_at(px + i * direction, py) is not None:
                    return False

            rook_position = (7 if direction == 1 else 0, py)
            rook_piece = game_state.board.piece_at(rook_position[0], rook_position[1])

            # Ensure there's a rook at the position, and it hasn't moved
            if isinstance(rook_piece, Rook) and not rook_piece.has_moved:
                return True

        return False

    def is_move_into_check(self, x: int, y: int, game_state: 'GameState') -> bool:
        """
        Determine if a move places the king in check.

        Args:
            x (int): The x-coordinate of the proposed move destination.
            y (int): The y-coordinate of the proposed move destination.
            game_state (GameState): The chess game's state.

        Returns:
            bool: True if the move would place the king in check, False otherwise.
        """
        if self.is_white:
            # Iterate through each list of moves in black_targets
            for moves in game_state.black_targets.values():
                # If the proposed move is in the legal moves of any black piece, the king is in check
                if (x, y) in moves:
                    return True
        else:
            # Similarly for white pieces
            for moves in game_state.white_targets.values():
                if (x, y) in moves:
                    return True

        # If no piece can legally move to the proposed coordinates, the king is not in check
        return False

    def is_in_check(self, game_state: 'GameState'):
        if self.is_white:
            # Iterate through each list of moves in black_targets
            for moves in game_state.black_targets.values():
                # If the current position is in the legal moves of any black piece, the king is in check
                if (self.x, self.y) in moves:
                    return True
        else:
            # Similarly for white pieces
            for moves in game_state.white_targets.values():
                if (self.x, self.y) in moves:
                    return True

        return False
