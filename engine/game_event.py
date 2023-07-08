from enum import Enum


class GameEvent(Enum):
    """
    Enumerates different events that can occur in a chess game.

    MOVE: Represents a standard piece move.
    CAPTURE: Represents a piece capture.
    CASTLE: Represents castling.
    PROMOTION: Represents pawn promotion.
    NOTIFICATION: Represents a game notification.
    CHECK: Represents a check.
    STALEMATE: Represents a stalemate.
    CHECKMATE: Represents a checkmate.
    """
    MOVE = 'move'
    CAPTURE = 'capture'
    CASTLE = 'castle'
    PROMOTION = 'promotion'
    NOTIFICATION = 'notification'
    CHECK = 'check'
    STALEMATE = 'stalemate'
    CHECKMATE = 'checkmate'

