import tkinter as tk
from pieces import Piece, Pawn
from utils.constants import piece_classes
from engine.game_event import GameEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import ChessUI


class PromotionUI:
    """
    A class that orchestrates the pawn promotion process by creating and managing a promotion selection UI.

    The class is responsible for initializing a promotion screen where users can choose which piece
    the pawn will be promoted to, either 'Queen', 'Rook', 'Bishop', or 'Knight'.

    Attributes:
        chess_ui (ChessUI): An instance of the main game user interface.
        _selected_promotion (Piece or None): The piece selected by the user for pawn promotion.
    """

    def __init__(self, chess_ui: 'ChessUI', pawn: Pawn):
        """
        Construct a new PromotionUI object and set up the promotion screen.

        Args:
            chess_ui (ChessUI): An instance of the main game UI.
            pawn (Pawn): The pawn piece that is about to be promoted.
        """
        self.chess_ui = chess_ui
        self._selected_promotion = None

        # An instance of GameEventNotifier (used to play promotion sounds upon promotion event)
        self.notifier = chess_ui.game.game_event_notifier

        self.create_promotion_screen()
        self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))

    @property
    def selected_promotion(self) -> type[Piece] or None:
        """
        Get the piece that has been selected for promotion.

        Returns:
            Piece or None: The piece that has been selected for promotion or None if no piece has been selected yet.
        """
        return self._selected_promotion

    @selected_promotion.setter
    def selected_promotion(self, piece: type[Piece] or None):
        """
        Set the piece to be promoted to upon user's selection.

        Args:
            piece (Piece or None): The selected piece to be promoted to, or None to reset the selection.
        """
        self._selected_promotion = piece

    def create_promotion_screen(self):
        """
        Set up and display the pawn promotion selection screen.

        This method initializes a new window with the promotion options,
        which the user can choose from: 'Queen', 'Rook', 'Bishop', or 'Knight'.
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
        Continually check if a promotion selection has been made.

        If a selection is made, promote the pawn and update the game status,
        otherwise, continue checking every 100ms.

        Args:
            pawn (Pawn): The pawn piece to be promoted.
        """
        if self.selected_promotion is None:  # if the promotion hasn't been selected yet, schedule the check again
            self.chess_ui.root.after(100, lambda: self.wait_for_promotion(pawn))  # checks every 100 ms
        else:
            promotion_piece = self.selected_promotion
            self.selected_promotion = None  # reset selected promotion

            self.chess_ui.game.engine.promote_from_ui(pawn, promotion_piece)  # promote the pawn
            self.notifier.notify(GameEvent.PROMOTION)  # promotion event notification
            self.chess_ui.update()  # update immediately after promotion
