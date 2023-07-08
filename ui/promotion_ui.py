import tkinter as tk

from engine import GameEvent
from pieces import Piece, Pawn
from ui.click_handler import GameEventNotifier
from utils import piece_classes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import ChessUI


class PromotionUI:
    """
    Handles the pawn promotion UI in the chess game.

    Manages UI display, user piece selection and subsequent game updates.
    """

    def __init__(self, chess_ui: 'ChessUI', pawn: Pawn, notifier: GameEventNotifier):
        """
        Initialize the promotion UI and start waiting for promotion selection.

        Args:
            chess_ui (ChessUI): Main game UI instance.
            pawn (Pawn): Pawn piece to be promoted.
            notifier (GameEventNotifier): Event notifier.
        """
        self.chess_ui = chess_ui
        self._selected_promotion = None
        self.notifier = notifier

        self.create_promotion_screen()
        self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))

    def create_promotion_screen(self):
        """
        Set up and display the pawn promotion selection screen.
        """
        # Notify that a promotion screen will pop up
        self.notifier.notify(GameEvent.NOTIFICATION)

        # Create a new window
        promotion_window = tk.Toplevel(self.chess_ui.root)

        # Set window title
        promotion_window.title("Promote Pawn")

        # Set window size
        promotion_window.geometry("300x200")
        
        # Center the window on the root canvas
        window_width = promotion_window.winfo_reqwidth()
        window_height = promotion_window.winfo_reqheight()
        position_x = int((self.chess_ui.root.winfo_screenwidth() / 2) - (window_width / 2))
        position_y = int((self.chess_ui.root.winfo_screenheight() / 2) - (window_height / 2))
        promotion_window.geometry(f"+{position_x}+{position_y}")

        # Create label
        label = tk.Label(promotion_window, text="Choose a piece to promote to:")
        label.pack()

        def select_piece(piece_selected: str):
            # Instead of returning the piece, set the selected_promotion member
            self.selected_promotion = piece_classes[piece_selected]
            promotion_window.destroy()

        # Piece options
        pieces = ['Queen', 'Rook', 'Bishop', 'Knight']
        # Create a button for each piece
        for piece_name in pieces:
            button = tk.Button(
                promotion_window,
                text=piece_name,
                command=lambda piece_selected=piece_name: select_piece(piece_selected)
            )
            button.pack()
            
    def wait_for_promotion(self, pawn: Pawn):
        """
        Check for promotion selection, promote the pawn and update the game. Method notifies game of promotion event
        after a promotion piece has been selected.

        Args:
            pawn (Pawn): The pawn piece to be promoted.
        """
        if self.selected_promotion is None:  # if the promotion hasn't been selected yet, schedule the check again
            self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))  # checks every 100 ms
        else:
            promotion_piece = self.selected_promotion
            self.selected_promotion = None  # reset selected promotion

            self.chess_ui.game_state.game_engine.promote(pawn, promotion_piece)  # promote the pawn
            self.notifier.notify(GameEvent.PROMOTION)  # promotion event notification
            self.chess_ui.update()  # update immediately after promotion

    @property
    def selected_promotion(self) -> Piece or None:
        """
        Get the currently selected promotion piece.

        Returns:
            Piece or None: Selected promotion piece or None if no piece has been selected.
        """
        return self._selected_promotion

    @selected_promotion.setter
    def selected_promotion(self, piece: Piece or None):
        """
        Set the selected promotion piece.

        Args:
            piece (Piece or None): Promotion piece to set or None to clear the selection.
        """
        self._selected_promotion = piece
