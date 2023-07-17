from __future__ import annotations
import copy
from typing import Optional

from engine.move import Move
from pieces import Piece, Queen
from pieces.king import King
from pieces.pawn import Pawn
from players import Player
from utils.type import TeamType, PieceType

from engine.game_event_notifier import GameEventNotifier
from engine.game_event import GameEvent
from engine.board import Board
from engine.game_engine import GameEngine
from engine.game_status import GameStatus
from engine.move_generator import MoveGenerator

from ui import ChessUI


class ChessGame:
    """
    A class to represent the Chess game. It encapsulates the game's players, current state, board, events,
    move generator, engine, and status.

    Attributes:
        players (list[Player]): The list of active players.
        _board (Board): The current game board.
        _event (GameEvent): The current game event.
        _move_generator (MoveGenerator): Generator for possible moves.
        _engine (GameEngine): Engine to handle game rules.
        _status (GameStatus): The status of the current game.
    """

    def __init__(self):
        """
        Initializes a Game with two players, a board, and a game engine.
        One player is human and the other is AI.
        A game event notifier is also set up for event handling.
        """
        self.players = [Player(name="player 1", team=TeamType.ALLY),
                        Player(name="player 2", team=TeamType.OPPONENT, is_human=False)]
        self.current_player = self.players[0]
        self.state = GameEvent.ONGOING
        self._board = Board()
        self._event = None
        self._move_generator = MoveGenerator(self)
        self._engine = GameEngine(self)
        self._status = GameStatus(self)
        self._game_event_notifier = GameEventNotifier()

        self.ui = ChessUI(self)
        self.ui.run()

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

    def make_move(self, piece: Piece, new_x: int, new_y: int, promotion_piece: Piece = None) -> bool:
        """
        Makes a move in the game. If the move is legal and successful, the turn is passed to the other player.

        Args:
            piece (Piece): The piece to move.
            new_x (int): The new x-coordinate for the piece.
            new_y (int): The new y-coordinate for the piece.
            promotion_piece (type[Piece]): The piece type to promote a pawn to if the move leads to a promotion. Defaults to None.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.state != GameEvent.ONGOING or piece.team != self.current_player.team:
            return False
        original_x, original_y = piece.x, piece.y

        if self.move_leads_to_promotion(piece, new_y):
            # If a promotion piece is not specified or is not a valid promotion piece, default to a queen
            if promotion_piece is None or isinstance(promotion_piece, (King, Pawn)):
                promotion_piece = Queen(x=piece.x, y=piece.y, team=piece.team, is_white=piece.is_white)
            move_successful = self.engine.move_piece(piece, new_x, new_y, promotion_piece=promotion_piece)
        else:
            promotion_piece = None
            move_successful = self.engine.move_piece(piece, new_x, new_y, promotion_piece)

        if move_successful:
            self.update_game_state(piece, original_x, original_y, new_x, new_y, promotion_piece)
            print(repr(self.engine.last_move))
            self.ui.update()  # Refresh the UI board after each move

        return move_successful

    def update_game_state(self, piece: Piece, original_x: int, original_y: int, new_x: int, new_y: int,
                          promotion_piece: Piece) -> list[GameEvent]:
        """
        Updates the game state after a move has been made. Also sets the last move details.

        Args:
            piece (Piece): The piece that moved.
            original_x (int): The original x-coordinate of the piece.
            original_y (int): The original y-coordinate of the piece.
            new_x (int): The new x-coordinate of the piece.
            new_y (int): The new y-coordinate of the piece.
            promotion_piece (Piece): The piece to which a pawn has been promoted, if applicable.

        Returns:
            list[GameEvent]: List of game events that occurred due to the move.
        """
        events = self.get_state(self.current_player.team)
        self.engine.last_move = Move(
            piece=piece,
            start_position=(original_x, original_y),
            end_position=(new_x, new_y),
            is_capture=GameEvent.CAPTURE in events,
            is_king_side_castle=GameEvent.KING_SIDE_CASTLE in events,
            is_queen_side_castle=GameEvent.QUEEN_SIDE_CASTLE in events,
            is_check=GameEvent.CHECK in events,
            is_stalemate=GameEvent.STALEMATE in events,
            is_checkmate=GameEvent.CHECKMATE in events,
            promotion=promotion_piece
        )
        if GameEvent.CHECKMATE in events or GameEvent.STALEMATE in events:
            self.state = events[0]

        return events

    def next_turn(self):
        """
        Ends the current player's turn and passes the turn to the other player.
        If the next player is an AI, the AI makes its move before the turn is passed back to the human player.
        """
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        if not self.current_player.is_human:
            move = self.current_player.ai_choose_move(self)

            if move != (None, -1, -1, None):
                cpu_piece, cpu_x, cpu_y, cpu_promotion_piece = move
                self.make_move(piece=cpu_piece,
                               new_x=cpu_x,
                               new_y=cpu_y,
                               promotion_piece=cpu_promotion_piece)
                self.next_turn()  # switch turn back to the human player after AI makes a move
            else:
                if self.is_game_over():
                    print(f"{self.get_winner().name} wins!")

    def is_game_over(self) -> bool:
        return self.state == GameEvent.CHECKMATE or self.state == GameEvent.STALEMATE

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
        # Temporarily store the UI object
        ui_temp = self.ui
        self.ui = None

        # Copy the game
        copied_game = copy.deepcopy(self)

        # The copied game does not have a UI object
        self.ui = ui_temp
        return copied_game

    def get_state(self, team: TeamType) -> list[GameEvent]:
        """
        Determines the game event based on the current board state and the last move.

        Args:
            team (TeamType): The team currently playing on the chessboard.

        Returns:
            GameEvent: The calculated game event.
        """
        enemy_team = TeamType.OPPONENT if team == TeamType.ALLY else TeamType.ALLY
        events = []
        if self.status.is_in_checkmate(enemy_team):  # Check if this team checkmated the opponent
            events.append(GameEvent.CHECKMATE)
        elif self.status.is_in_check(enemy_team):  # Check if this team checked the opponent
            events.append(GameEvent.CHECK)
        elif self.status.is_in_stalemate(enemy_team):  # Check if this team stalemated the opponent
            events.append(GameEvent.STALEMATE)

        if self.event == GameEvent.CAPTURE:  # Check if this team captured a piece
            events.append(self.event)
        if self.event == GameEvent.KING_SIDE_CASTLE or \
                self.event == GameEvent.QUEEN_SIDE_CASTLE:  # Check if this team castled
            events.append(self.event)
        if self.status.was_pawn_recently_promoted():  # Check if this team promoted
            events.append(self.event)
        events.append(GameEvent.MOVE)  # If none of the above checks passed, assume a normal move occurred
        return events

    @staticmethod
    def move_leads_to_promotion(piece: Piece, new_y: int) -> bool:
        """
        Checks if the given move, when made, will lead to the promotion of a pawn.
        A pawn can be promoted when it is about to move to the opponent's end of the board
        (the 8th rank for white pawns or the 1st rank for black pawns).

        Args:
            piece (Piece): The piece to move.
            new_y (int): The new y-coordinate for the piece.

        Returns:
            bool: True if the move leads to a promotion, False otherwise.
        """
        if piece.type == PieceType.PAWN:
            if piece.team == TeamType.ALLY and new_y == 0:  # For white pawns
                return True
            elif piece.team == TeamType.OPPONENT and new_y == 7:  # For black pawns
                return True

        return False
