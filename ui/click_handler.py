import tkinter as tk
from ui.promotion_ui import PromotionUI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess_ui import ChessUI
    
    
class ClickHandler:
    """
    Class to handle mouse click events in the ChessUI.

    Attributes:
        chess_ui (ChessUI): The chess user interface instance this handler is bound to.
    """

    def __init__(self, chess_ui: 'ChessUI'):
        """
        Initialize the ClickHandler with a given ChessUI.

        Args:
            chess_ui (ChessUI): The chess user interface instance this handler is bound to.
        """
        self.chess_ui = chess_ui

    def handle_click(self, event: tk.Event):
        """
        Handles a mouse click event. If no piece is selected, selects a piece. 
        If a piece is selected, tries to move it.

        Args:
            event (tkinter.Event): The event object.
        """
        chess_ui = self.chess_ui

        if chess_ui.first_click is None:
            x = (event.x - 50) // 100
            y = (event.y - 50) // 100
            piece = chess_ui.game_state.board.piece_at(x, y)
            if piece is not None:
                chess_ui.first_click = (x, y)
                chess_ui.selected_piece = piece
                chess_ui.calculate_legal_moves(piece)
        else:
            x, y = chess_ui.first_click
            new_x = (event.x - 50) // 100
            new_y = (event.y - 50) // 100
            piece = chess_ui.game_state.board.piece_at(x, y)
            chess_ui.first_click = None

            if (new_x, new_y) in chess_ui.legal_moves:
                chess_ui.game_state.move_piece(piece, new_x, new_y)
                
                if chess_ui.game_state.is_promotion():
                    PromotionUI(chess_ui=chess_ui, pawn=piece)
                    
            chess_ui.selected_piece = None
            chess_ui.legal_moves = []
            chess_ui.update()