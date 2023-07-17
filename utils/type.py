from enum import Enum


class PieceType(Enum):
    """
    An enumeration representing the types of pieces in a chess game.

    Attributes:
        PAWN: Represents a pawn piece.
        KNIGHT: Represents a knight piece.
        BISHOP: Represents a bishop piece.
        ROOK: Represents a rook piece.
        QUEEN: Represents a queen piece.
        KING: Represents a king piece.
    """
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class TeamType(Enum):
    """
    An enumeration representing the teams in a chess game.

    Attributes:
        OPPONENT: Represents the opponent's team.
        ALLY: Represents the player's team.
    """
    OPPONENT = 1
    ALLY = 2
