from board import Board
from pieces import King


class GameState:
    """
    A class used to represent the current state of a Chess game.

    Attributes:
        board (Board): A Board object representing the current state of the chess board.
    """

    def __init__(self, board: Board):
        """
        Initializes a GameState with a given Board object.

        Args:
            board (Board): A Board object representing the current state of the chess board.
        """
        self.board = board
        
    def is_checkmate(self):
        # Get the current player
        current_player = self.get_current_player()

        # Get the opponent's pieces
        opponent_pieces = self.get_opponent_pieces()

        # Get the current player's king
        king = self.get_king(current_player)

        # Check if the king is in check
        if not king.is_in_check(opponent_pieces):
            return False

        # Check if the king has any safe squares to move to
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x = king.x + dx
                new_y = king.y + dy
                if self.board.is_valid_position(new_x, new_y):
                    if not self.board.is_square_under_attack(new_x, new_y, opponent_pieces):
                        return False

        # Check if any of the current player's pieces can block the check
        for piece in self.get_current_player_pieces():
            if isinstance(piece, King):
                continue
            if piece.can_block_check(king, opponent_pieces):
                return False

        # If none of the conditions are met, it's a checkmate
        return True
    
    def get_current_player(self):
        pass
    
    def get_opponent_pieces(self):
        pass
    
    def get_king(self):
        pass
    
    def get_current_player_pieces(self):
        pass
    
    def is_promotion(self):
        pass
