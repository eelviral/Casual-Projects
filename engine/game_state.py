import copy

from engine.game_event import GameEvent
from engine.board import Board
from engine.game_engine import GameEngine
from engine.game_status import GameStatus
from engine.move_generator import MoveGenerator
from pieces import Piece
from utils import TeamType


class GameState:
    """
    Represents the current state of a Chess game, encapsulating the game's board, event,
    move generator, engine, and status.

    Attributes:
        _board (Board): The current game board.
        _event (GameEvent): The current game event.
        _move_generator (MoveGenerator): Generator for possible moves.
        _game_engine (GameEngine): Engine to handle game rules.
        _game_status (GameStatus): The status of the current game.
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a Board.

        Args:
            board (Board): The current chess board.
        """
        self._board = board
        self._event = None
        self._move_generator = MoveGenerator(self)
        self._game_engine = GameEngine(self)
        self._game_status = GameStatus(self)

    @property
    def board(self) -> Board:
        """
        Returns the current state of the chess board.

        Returns:
            Board: Current chess board configuration.
        """
        return self._board

    @property
    def event(self) -> GameEvent:
        """
        Returns the last event in the game.

        Returns:
            GameEvent: The last game event.
        """
        return self._event

    @event.setter
    def event(self, e: GameEvent):
        """
        Sets the last event in the game.

        Args:
            e (GameEvent): The game event to set.
        """
        self._event = e

    def get_state(self, piece_moved: Piece) -> GameEvent:
        """
        Determines the game event based on the current board state and the last move.

        Args:
            piece_moved (Piece): The piece that moved last.

        Returns:
            GameEvent: The calculated game event.
        """
        enemy_team = TeamType.OPPONENT if piece_moved.team == TeamType.ALLY else TeamType.ALLY
        if self.game_status.is_in_checkmate(enemy_team):
            return GameEvent.CHECKMATE
        elif self.game_status.is_in_check(enemy_team):
            return GameEvent.CHECK
        elif self.game_status.is_in_stalemate(enemy_team):
            return GameEvent.STALEMATE
        elif self.event == GameEvent.CAPTURE:
            return self.event
        elif self.event == GameEvent.CASTLE:
            return self.event
        elif self.game_engine.is_promotion():
            return self.event
        return GameEvent.MOVE

    @property
    def move_generator(self):
        """
        Returns the MoveGenerator for calculating possible moves.

        Returns:
            MoveGenerator: The MoveGenerator instance.
        """
        return self._move_generator

    @property
    def game_engine(self):
        """
        Returns the GameEngine for applying game rules.

        Returns:
            GameEngine: The GameEngine instance.
        """
        return self._game_engine

    @property
    def game_status(self):
        """
        Returns the GameStatus for monitoring the current game status.

        Returns:
            GameStatus: The GameStatus instance.
        """
        return self._game_status

    def copy(self):
        """
        Creates a deep copy of the game state.

        Returns:
            GameState: A new GameState instance with the same state.
        """
        return copy.deepcopy(self)
