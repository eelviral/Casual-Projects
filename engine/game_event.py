from enum import Enum


class GameEvent(Enum):
    MOVE = 'move'
    CAPTURE = 'capture'
    CASTLE = 'castle'
    PROMOTION = 'promotion'
    NOTIFICATION = 'notification'
    CHECK = 'check'
    CHECKMATE = 'checkmate'
