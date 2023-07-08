from collections import Counter
from utils import TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import GameState


class GameStatus:
    """
    A class to represent the status of a chess game. This class provides utility methods
    to check game conditions like check and checkmate.

    Attributes:
        game_state (GameState): The current state of the game.
        board (Board): The current state of the chess board.
        move_generator (MoveGenerator): A generator for possible moves in the game.
    """

    def __init__(self, game_state: 'GameState'):
        """
        Constructs a new game status with the given game state.

        Args:
            game_state (GameState): The initial game state.
        """
        self.game_state = game_state
        self.board = game_state.board
        self.move_generator = game_state.move_generator
        self.positions = []

    def is_in_check(self, team: TeamType):
        """
        Checks if a king is in check.

        Args:
            team (TeamType): The team of the king to check.

        Returns:
            bool: True if the king is in check, False otherwise.
        """
        king = self.board.get_king(team)

        # Check each enemy piece if they can reach the king's position
        for piece in self.board.pieces:
            if piece.team != team:
                if piece.is_controlled_square(piece.x, piece.y, king.x, king.y, self.game_state):
                    return True
        return False

    def is_in_checkmate(self, team: TeamType) -> bool:
        """
        Checks if the king of a given team is in checkmate.

        Args:
            team (TeamType): The team of the king to check.

        Returns:
            bool: True if the king is in checkmate, False otherwise.
        """
        # First, check if the king is in check
        if not self.is_in_check(team):
            return False

        # Then, check if there are any legal moves left that would result in the king not being in check
        for piece in self.board.pieces:
            if piece.team == team:
                if self.move_generator.calculate_legal_moves_for_piece(piece):
                    return False

        # If there are no such moves, the king is in checkmate
        return True

    def is_in_stalemate(self, team: TeamType) -> bool:
        """
        Checks if the king of a given team is in stalemate.

        Args:
            team (TeamType): The team of the king to check.

        Returns:
            bool: True if the king is in stalemate, False otherwise.
        """
        if self.is_threefold_repetition():
            return True

        # First, check if the king is NOT in check
        if self.is_in_check(team):
            return False

        # Then, check if there are any legal moves left for any piece of the team
        for piece in self.board.pieces:
            if piece.team == team:
                if self.move_generator.calculate_legal_moves_for_piece(piece):
                    return False

        # If there are no such moves and the king is not in check, it is stalemate
        return True

    def is_threefold_repetition(self) -> bool:
        """
        Checks if the current position has occurred three times in the game.

        Returns:
            bool: True if the current position has occurred three times, False otherwise.
        """
        positions_counter = Counter(self.positions)
        return positions_counter[self.board.fen()] >= 3
