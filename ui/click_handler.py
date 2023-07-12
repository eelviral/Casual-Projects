import tkinter as tk
from ui.promotion_ui import PromotionUI
from ui.sound_player import SoundPlayer
from utils import TeamType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui import ChessUI


class ClickHandler:
    """
    A class responsible for managing the interaction between the user's mouse clicks and the chess game.
    This class processes the clicks, selects and moves pieces, and triggers game events accordingly.

    Attributes:
        chess_ui (ChessUI): An instance of the chess user interface that this handler is interacting with.
    """

    def __init__(self, chess_ui: 'ChessUI'):
        """
        Initialize the ClickHandler with a given ChessUI and a GameEventNotifier to manage game events.

        Args:
            chess_ui (ChessUI): The chess user interface instance this handler is interacting with.
        """
        self.chess_ui = chess_ui
        self.board = chess_ui.game.board

        # An instance of GameEventNotifier to notify subscribers of game events
        self.notifier = GameEventNotifier()

        # Create and subscribe a sound player to the notifier
        sound_player = SoundPlayer()
        self.notifier.subscribe(sound_player)

    def handle_click(self, event: tk.Event):
        """
        Manages a mouse click event. If no piece is currently selected, it selects a piece.
        If a piece is selected, it tries to move it and notifies subscribers of game events.

        If the selected piece is a pawn and moves to the opposite end of the board, a PromotionUI instance
        is created to handle the pawn promotion event.

        Args:
            event (tkinter.Event): The event object containing information about the mouse click.
        """
        chess_ui = self.chess_ui

        if chess_ui.first_click is None:
            x = (event.x - 50) // 100
            y = (event.y - 50) // 100
            piece = self.board.piece_at(x, y)

            # Don't store click if the square is empty or if it's not the selected piece's turn yet
            # (Prevents highlighted squares from showing up for the wrong team)
            if piece is not None and chess_ui.game.current_player.team == piece.team:
                chess_ui.first_click = (x, y)
                chess_ui.selected_piece = piece
                chess_ui.calculate_legal_moves(piece)
        else:
            x, y = chess_ui.first_click
            new_x = (event.x - 50) // 100
            new_y = (event.y - 50) // 100
            piece = self.board.piece_at(x, y)
            chess_ui.first_click = None

            if (new_x, new_y) in chess_ui.legal_moves:
                chess_ui.game.make_move(piece, new_x, new_y)
                enemy_team = TeamType.OPPONENT if piece.team == TeamType.ALLY else TeamType.ALLY
                event = self.chess_ui.game.get_state(enemy_team)

                # Notifies subscribers of the game event
                self.notifier.notify(event)

                if chess_ui.game.status.is_promotion():
                    # Handles promotion selection and promotion sound effect
                    PromotionUI(chess_ui=chess_ui, pawn=piece)

            chess_ui.selected_piece = None
            chess_ui.legal_moves = []
            chess_ui.update()
