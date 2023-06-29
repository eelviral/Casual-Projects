import tkinter as tk
from game_state import GameState
from pieces import Piece
from ui import *

WHITE_IMAGES = 'images/white/'
BLACK_IMAGES = 'images/black/'


class ChessUI:
    """
    A class to represent the user interface for a chess game.

    Attributes:
        game_state (GameState): The current state of the game.
        root (Tk): The root Tkinter instance.
        canvas (Canvas): The Tkinter canvas to draw the game on.
        images (dict): Dictionary mapping piece symbols to their images.
        first_click (tuple): The coordinates of the first click, or None if no click has been made yet.
        selected_piece (Piece): The selected piece, or None if no piece is selected.
        legal_moves (list): List of current legal moves.
    """

    def __init__(self, game_state: GameState):
        """
        Initialize the ChessUI with a given game state.

        Args:
            game_state (GameState): The current state of the game.
        """
        self.game_state = game_state
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=900, height=900)
        self.canvas.pack()

        # Load images
        self.images = self.__load_images()

        # Event handling
        self.first_click = None
        self.selected_piece = None
        self.legal_moves = []
        self.click_handler = ClickHandler(self)
        self.canvas.bind("<Button-1>", self.click_handler.handle_click)

    def calculate_legal_moves(self, piece: Piece):
        """
        Calculate the legal moves for a given piece and update the game board.

        Args:
            piece (Piece): The piece to calculate legal moves for.
        """
        self.legal_moves = self.game_state.calculate_legal_moves_for_piece(piece)
        self.update()  # Update immediately after calculating legal moves

    @staticmethod
    def __load_images() -> dict:
        """
        Load images for each chess piece.

        Returns:
            dict: A dictionary mapping piece symbols to their images.
        """
        images = {}
        pieces = {
            'pawn': 'P',
            'knight': 'N',
            'bishop': 'B',
            'rook': 'R',
            'queen': 'Q',
            'king': 'K'
        }

        for piece, symbol in pieces.items():
            images[symbol.upper()] = tk.PhotoImage(file=f'{WHITE_IMAGES}{piece}.png')
            images[symbol.lower()] = tk.PhotoImage(file=f'{BLACK_IMAGES}{piece}.png')
        return images

    def draw_board(self):
        """Draw the chess board on the canvas, and highlighting for any legal moves."""
        for i in range(8):
            for j in range(8):
                x1 = i * 100 + 50
                y1 = j * 100 + 50
                x2 = x1 + 100
                y2 = y1 + 100
                color = "#deb887" if (i + j) % 2 == 0 else "#4d3222"
                if (i, j) in self.legal_moves:
                    color = "#00ff00"  # Highlight with green color for legal moves
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_pieces(self):
        """Draw the chess pieces on the board using the images loaded previously."""
        board = self.game_state.board
        for piece in board:
            if piece is not None:
                x = (piece.x + 0.5) * 100 + 50
                y = (piece.y + 0.5) * 100 + 50
                image = self.images.get(piece.symbol)
                if image is not None:
                    self.canvas.create_image(x, y, image=image, anchor=tk.CENTER)

    def draw_labels(self):
        """Draw labels for the chess board columns and rows."""
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in range(8):
            x = i * 100 + 100
            y = 25
            self.canvas.create_text(x, y, text=labels[i])
            y = 875
            self.canvas.create_text(x, y, text=labels[i])
            x = 25
            y = i * 100 + 100
            self.canvas.create_text(x, y, text=8 - i)
            x = 875
            self.canvas.create_text(x, y, text=8 - i)

    def update(self):
        """
        Update the chess board and pieces.
        
        Deletes all canvas content and redraws the board, pieces and labels.
        """
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_labels()

    def run(self):
        """Start the Tkinter event loop."""
        self.update()
        self.root.mainloop()
