from pieces import Piece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import GameState


class MoveGenerator:
    """
    A class to generate legal moves in a chess game.

    This class is responsible for generating all the legal moves that can be made by a piece.
    It checks not only the rules of movement for the piece, but also whether the move would
    put the player's own king in check.

    Attributes:
        game_state (GameState): The current state of the game.

    """

    def __init__(self, game_state: 'GameState'):
        """
        Constructs a new MoveGenerator object with the given game state.

        Args:
            game_state (GameState): The initial game state.
        """
        self.game_state = game_state

    def calculate_legal_moves_for_piece(self, piece: Piece) -> list[tuple[int, int]]:
        """
        Calculates all legal moves for a given piece.

        Args:
            piece (Piece): The piece to calculate legal moves for.

        Returns:
            list[tuple[int, int]]: List of legal moves, each move is represented by a tuple (x, y).
        """
        legal_moves = []

        # Generate all possible moves for the piece
        possible_moves = []
        for i in range(8):
            for j in range(8):
                # If the move is legal and either the king is not in check or the move protects the king
                if piece.legal_move(px=piece.x, py=piece.y, x=i, y=j, game_state=self.game_state):
                    possible_moves.append((i, j))

        for x, y in possible_moves:
            # Create a temporary copy of the game state and make the move
            temp_state = self.game_state.copy()
            temp_piece = temp_state.board.piece_at(x=piece.x, y=piece.y)

            # If the move results in a successful move and doesn't cause a check, add it to the legal moves
            if temp_state.game_engine.move_piece(piece=temp_piece, new_x=x, new_y=y) and \
                    not temp_state.game_status.is_in_check(piece.team):
                legal_moves.append((x, y))

        return legal_moves

    def move_protects_king(self, px: int, py: int, x: int, y: int) -> bool:
        """
        Checks if a proposed move would result in the current player's King being in check.

        The method creates a temporary copy of the game state, makes the proposed move in this copied game state,
        and then checks if the resulting state would put the King in check. The real game state remains unaffected.

        Args:
            px (int): The current x-coordinate of the piece that is proposed to be moved.
            py (int): The current y-coordinate of the piece that is proposed to be moved.
            x (int): The proposed new x-coordinate for the piece.
            y (int): The proposed new y-coordinate for the piece.

        Returns:
            bool: True if the proposed move would not result in the King being in check, False otherwise.
        """
        temp_state = self.game_state.copy()
        temp_piece = temp_state.board.piece_at(x=px, y=py)
        temp_state.game_engine.move_piece(piece=temp_piece, new_x=x, new_y=y)
        return not temp_state.game_status.is_in_check(temp_piece.team)
