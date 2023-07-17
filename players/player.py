import random
from pieces import Queen, Rook, Bishop, Knight
from pieces.piece import Piece
from utils import TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import ChessGame


class Player:
    """
    A class to represent a player in the game of Chess.
    """

    def __init__(self, name: str, team: TeamType, is_human: bool = True):
        """
        Initializes a Player with a name and a team.

        Args:
            name (str): The name of the player.
            team (TeamType): The team that the player belongs to.
        """
        self.name = name
        self.team = team

        # Player is assumed to be human unless specified
        self._is_human = is_human

    @property
    def is_human(self) -> bool:
        return self._is_human

    @is_human.setter
    def is_human(self, value: bool):
        self._is_human = value

    def ai_choose_move(self, game: 'ChessGame') -> tuple[Piece, int, int, Piece]:
        legal_moves = game.move_generator.current_team_legal_moves()
        if legal_moves == []:
            return None, -1, -1, None
        
        move = random.choice(legal_moves)
        
        piece = move[0]
        x = move[1][0]
        y = move[1][1]
        
        promotion_pieces = [Queen(x, y, piece.team, piece.is_white),
                            Rook(x, y, piece.team, piece.is_white),
                            Bishop(x, y, piece.team, piece.is_white),
                            Knight(x, y, piece.team, piece.is_white)]
        promotion_piece = random.choice(promotion_pieces)
        return piece, x, y, promotion_piece
    