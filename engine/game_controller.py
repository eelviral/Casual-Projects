import copy
from typing import Optional
from engine.game_event import GameEvent
from engine.game_state import GameState
from pieces import Piece
from players import Player
from utils import TeamType


class GameController:
    """
    A class to represent the controller of a Chess game.

    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
    """

    def __init__(self, game_state: GameState):
        """
        Initializes a Game with two players and a game engine.

        Args:
            game_state (GameState): The game state to determine the state of the game.
        """

        self.players = [Player(name="player 1", team=TeamType.ALLY), Player(name="player 2", team=TeamType.OPPONENT)]
        self.game_state = game_state
        self.current_player = self.players[0]
        self.status = GameEvent.ONGOING

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
        if self.status != GameEvent.ONGOING or piece.team != self.current_player.team:
            return False

        move_successful = self.game_state.game_engine.move_piece(piece, new_x, new_y)
        if move_successful:
            self.next_turn()
            self.check_game_over()

        return move_successful

    def check_game_over(self):
        """
        Checks if the game is over (i.e., if the current player is in checkmate or stalemate).
        """
        status = self.game_state.get_state(self.current_player.team)
        if status == GameEvent.CHECKMATE or status == GameEvent.STALEMATE:
            self.status = status

    def get_winner(self) -> Optional[Player]:
        """
        Returns the winner of the game, if there is one.

        Returns:
            Optional[Player]: The winner of the game. Returns None if the game is ongoing or ended in a draw.
        """
        if self.status == GameEvent.CHECKMATE:
            return self.players[1] if self.current_player == self.players[0] else self.players[0]
        return None

    def copy(self):
        """
        Creates a copy of the current game.

        Returns:
            GameController: A copy of the current game.
        """
        return copy.deepcopy(self)

    def get_legal_moves(self) -> list[tuple[Piece, tuple[int, int]]]:
        """
        Calculates all legal moves for the current team.

        Returns:
            list[tuple[Piece, tuple[int, int]]]: List of legal moves, each move is represented by a tuple
            where the first element is the piece and the second element is a tuple (x, y) representing
            the new position.
        """
        return [(piece, move) for piece in self.game_state.board.pieces if piece.team == self.current_player.team
                for move in self.game_state.move_generator.calculate_legal_moves_for_piece(piece)]
