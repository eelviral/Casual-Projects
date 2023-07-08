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
    A class used to represent the current state of a Chess game.

    This class contains all the necessary information for representing a game at a certain point,
    including the state of the board, the last move made, and functionality for calculating possible
    moves and determining the status of the game (like whether a player is in check).

    Attributes:
        board (Board): A Board object representing the current state of the chess board.
        event (GameEvent): A GameEvent enum representing an event in the game.
        move_generator (MoveGenerator): A MoveGenerator object to calculate possible moves.
        game_engine (GameEngine): A GameEngine object to handle the rules of the game.
        game_status (GameStatus): A GameStatus object to monitor the status of the game.
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a given Board object.

        Args:
            board (Board): A Board object representing the current state of the chess board.
        """
        self._board = board
        self._event = None

        self._move_generator = MoveGenerator(self)
        self._game_engine = GameEngine(self)
        self._game_status = GameStatus(self)

    @property
    def board(self) -> Board:
        """
        Provides the current state of the chess board. The state includes the positions and
        types of all pieces on the board.

        Returns:
            Board: A Board object representing the current chess board configuration.
        """
        return self._board

    @property
    def event(self) -> GameEvent:
        return self._event

    @event.setter
    def event(self, e: GameEvent):
        self._event = e

    def get_state(self, piece_moved: Piece) -> GameEvent:
        enemy_team = TeamType.OPPONENT if piece_moved.team == TeamType.ALLY else TeamType.ALLY
        if self.game_status.is_in_check(enemy_team):
            return GameEvent.CHECK
        elif self.game_status.is_in_checkmate(enemy_team):
            return GameEvent.CHECKMATE
        elif self.event == GameEvent.CAPTURE:
            return self.event
        elif self.event == GameEvent.CASTLE:
            return self.event
        elif self.game_engine.is_promotion():
            # Promotion events are activated only after a piece is selected in PromotionUI
            # For now, the game determines this to be a regular move
            return self.event
        return GameEvent.MOVE

    @property
    def move_generator(self):
        """
        Provides access to the MoveGenerator instance. The MoveGenerator calculates possible moves
        for pieces on the board according to the rules of chess.

        Returns:
            MoveGenerator: The MoveGenerator instance associated with this game state.
        """
        return self._move_generator

    @property
    def game_engine(self):
        """
        Provides access to the GameEngine instance. The GameEngine implements the rules of chess,
        allowing pieces to be moved on the board and determining the result of the game.

        Returns:
            GameEngine: The GameEngine instance associated with this game state.
        """
        return self._game_engine

    @property
    def game_status(self):
        """
        Provides access to the GameStatus instance. The GameStatus monitors the current status of
        the game, including whether players are in check or checkmate.

        Returns:
            GameStatus: The GameStatus instance associated with this game state.
        """
        return self._game_status

    def copy(self):
        """
        Creates a deep copy of the game state. This includes the board, last move, move generator,
        game engine, and game status.

        Returns:
            GameState: A new GameState instance with the same state as the current one.
        """
        new_game_state = copy.deepcopy(self)
        return new_game_state
