from __future__ import annotations
import copy
from typing import Optional
from pieces import Piece
from players import Player
from utils.type import TeamType

from engine.game_event_notifier import GameEventNotifier
from engine.game_event import GameEvent
from engine.board import Board
from engine.game_engine import GameEngine
from engine.game_status import GameStatus
from engine.move_generator import MoveGenerator


class ChessGame:
    """
    A class to represent the Chess game. It encapsulates the game's players, current state, board, events,
    move generator, engine, and status.

    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
        _board (Board): The current game board.
        _event (GameEvent): The current game event.
        _move_generator (MoveGenerator): Generator for possible moves.
        _engine (GameEngine): Engine to handle game rules.
        _status (GameStatus): The status of the current game.
    """

    def __init__(self):
        """
        Initializes a Game with two players, a board, and a game engine.
        """
        self.players = [Player(name="player 1", team=TeamType.ALLY), Player(name="player 2", team=TeamType.OPPONENT)]
        self.current_player = self.players[0]
        self.state = GameEvent.ONGOING
        self._board = Board()
        self._event = None
        self._move_generator = MoveGenerator(self)
        self._engine = GameEngine(self)
        self._status = GameStatus(self)
        self._game_event_notifier = GameEventNotifier()

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

    @property
    def game_event_notifier(self) -> GameEventNotifier:
        """
        Returns the game event notifier of the game.

        Returns:
            GameEventNotifier: The game event notifier.
        """
        return self._game_event_notifier

    @property
    def move_generator(self) -> MoveGenerator:
        """
        Returns the MoveGenerator for calculating possible moves.

        Returns:
            MoveGenerator: The MoveGenerator instance.
        """
        return self._move_generator

    @property
    def engine(self) -> GameEngine:
        """
        Returns the GameEngine for applying game rules.

        Returns:
            GameEngine: The GameEngine instance.
        """
        return self._engine

    @property
    def status(self) -> GameStatus:
        """
        Returns the GameStatus for monitoring the current game status.

        Returns:
            GameStatus: The GameStatus instance.
        """
        return self._status

    def next_turn(self):
        """
        Ends the current player's turn and passes the turn to the other player.
        """
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def make_move(self, piece: Piece, new_x: int, new_y: int) -> bool:
        """
        Makes a move in the game. If the move is legal and successful, the turn is passed to the other player.

        Args:
            piece (Piece): The piece to move.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.state != GameEvent.ONGOING or piece.team != self.current_player.team:
            return False

        move_successful = self.engine.move_piece(piece, new_x, new_y)
        if move_successful:
            self.next_turn()
            self.check_game_over()

        return move_successful

    def check_game_over(self):
        """
        Checks if the game is over (i.e., if the current player is in checkmate or stalemate).
        """
        state = self.get_state(self.current_player.team)
        if state == GameEvent.CHECKMATE or state == GameEvent.STALEMATE:
            self.state = state

    def get_winner(self) -> Optional[Player]:
        """
        Returns the winner of the game, if there is one.

        Returns:
            Optional[Player]: The winner of the game. Returns None if the game is ongoing or ended in a draw.
        """
        if self.state == GameEvent.CHECKMATE:
            return self.players[1] if self.current_player == self.players[0] else self.players[0]
        return None

    def copy(self) -> ChessGame:
        """
        Creates a copy of the current game.

        Returns:
            ChessGame: A copy of the current game.
        """
        return copy.deepcopy(self)

    def current_team_legal_moves(self) -> list[tuple[Piece, tuple[int, int]]]:
        """
        Calculates all legal moves for the current team.

        Returns:
            list[tuple[Piece, tuple[int, int]]]: List of legal moves, each move is represented by a tuple
            where the first element is the piece and the second element is a tuple (x, y) representing
            the new position.
        """
        return [(piece, move) for piece in self.board.pieces if piece.team == self.current_player.team
                for move in self.move_generator.piece_legal_moves(piece)]

    def get_state(self, team: TeamType) -> GameEvent:
        """
        Determines the game event based on the current board state and the last move.

        Args:
            team (TeamType): The team currently playing on the chessboard.

        Returns:
            GameEvent: The calculated game event.
        """
        if self.status.is_in_checkmate(team):
            return GameEvent.CHECKMATE
        elif self.status.is_in_check(team):
            return GameEvent.CHECK
        elif self.status.is_in_stalemate(team):
            return GameEvent.STALEMATE
        elif self.event == GameEvent.CAPTURE:
            return self.event
        elif self.event == GameEvent.CASTLE:
            return self.event
        elif self.status.is_promotion():
            return self.event
        return GameEvent.MOVE
