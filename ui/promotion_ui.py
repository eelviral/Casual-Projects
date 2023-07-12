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
    Handles the pawn promotion user interface (UI) in the chess game.

    The PromotionUI class is responsible for setting up and displaying the
    promotion selection screen when a pawn reaches the other side of the chessboard.
    It manages UI display, handles user piece selection, and communicates with the
    main game UI to apply the promotion.

    Attributes
    """

    def __init__(self, chess_ui: 'ChessUI', pawn: Pawn):
        """
        Initialize the promotion UI and start waiting for the user's promotion selection.

        Args:
            chess_ui (ChessUI): An instance of the main game UI.
            pawn (Pawn): The pawn piece that is about to be promoted.
        """
        self.chess_ui = chess_ui
        self._selected_promotion = None
        self.notifier = chess_ui.game_controller.game_state.game_event_notifier

        self.create_promotion_screen()
        self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))

    def create_promotion_screen(self):
        """
        Set up and display the pawn promotion selection screen.

        This method initializes a new window with the promotion options.
        The user can choose from 'Queen', 'Rook', 'Bishop', 'Knight'.
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
        Check if the user has made a promotion selection.

        This method continuously checks if the user has selected a promotion piece.
        Once the selection is made, the method promotes the pawn, updates the game,
        and notifies the game of the promotion event.

        Args:
            pawn (Pawn): The pawn piece to be promoted.
        """
        if self.selected_promotion is None:  # if the promotion hasn't been selected yet, schedule the check again
            self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))  # checks every 100 ms
        else:
            promotion_piece = self.selected_promotion
            self.selected_promotion = None  # reset selected promotion

            self.chess_ui.game_controller.game_state.game_engine.promote(pawn, promotion_piece)  # promote the pawn
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
