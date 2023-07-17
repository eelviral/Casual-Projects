from pieces import Piece, Queen, Rook, Bishop, Knight
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import ChessGame


class MoveGenerator:
    """
    A class to generate legal moves in a chess game.

    This class is responsible for generating all the legal moves that can be made by a piece.
    It checks not only the rules of movement for the piece, but also whether the move would
    put the player's own king in check.

    Attributes:
        game (ChessGame): The chess game being played.

    """

    def __init__(self, chess_game: 'ChessGame'):
        """
        Constructs a new MoveGenerator object with the given chess game.

        Args:
            chess_game (ChessGame): The chess game being played.
        """
        self.game = chess_game

    def piece_legal_moves(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Calculates all legal moves for a given piece.

        Args:
            piece (Piece): The piece to calculate legal moves for.

        Returns:
            list[tuple[int, int]]: List of legal moves, each move is represented by a tuple (x, y).
        """
        legal_moves = []

        # Generate all possible moves for the piece
        for i in range(8):
            for j in range(8):
                # If the move is legal and either the king is not in check or the move protects the king
                if piece.legal_move(px=piece.x, py=piece.y, x=i, y=j, chess_game=self.game) and \
                        self._move_protects_king(px=piece.x, py=piece.y, x=i, y=j):
                    legal_moves.append((i, j))

        return legal_moves

    def _move_protects_king(self, px: int, py: int, x: int, y: int) -> bool:
        """
        Checks if a proposed move would result in the current player's King being in check.

        The method creates a temporary copy of the chess game, makes the proposed move in this copied game state,
        and then checks if the resulting board would put the King in check. The real chess game remains unaffected.

        Args:
            px (int): The current x-coordinate of the piece that is proposed to be moved.
            py (int): The current y-coordinate of the piece that is proposed to be moved.
            x (int): The proposed new x-coordinate for the piece.
            y (int): The proposed new y-coordinate for the piece.

        Returns:
            bool: True if the proposed move would not result in the King being in check, False otherwise.
        """
        temp_game = self.game.copy()
        temp_piece = temp_game.board.piece_at(x=px, y=py)
        temp_game.engine.move_piece(piece=temp_piece, new_x=x, new_y=y)
        return not temp_game.status.is_in_check(temp_piece.team)

    def current_team_legal_moves(self) -> list[tuple[Piece, tuple[int, int]]]:
        """
        Calculates all legal moves for the current team.

        Returns:
            list[tuple[Piece, tuple[int, int]]]: List of legal moves, each move is represented by a tuple
            where the first element is the piece and the second element is a tuple (x, y) representing
            the new position.
        """
        return [(piece, move) for piece in self.game.board.pieces if piece.team == self.game.current_player.team
                for move in self.piece_legal_moves(piece)]
