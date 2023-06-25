import tkinter as tk
from game_state import GameState

WHITE_IMAGES = 'images/white/'
BLACK_IMAGES = 'images/black/'


class ChessUI:
    """A class to represent the user interface for a chess game."""

    def __init__(self, game_state: GameState):
        """Initialize the ChessUI with a given game state."""
        self.game_state = game_state
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=900, height=900)
        self.canvas.pack()

        # Load images
        self.images = self.__load_images()
        
        # Event handling
        self.first_click = None
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        """
        Handles a mouse click event.

        Args:
            event (tkinter.Event): The event object.
        """
        if self.first_click is None:
            x = (event.x - 50) // 100
            y = (event.y - 50) // 100
            piece = self.get_piece_at(x, y)
            if piece is not None:
                self.first_click = (x, y)
        else:
            x, y = self.first_click
            new_x = (event.x - 50) // 100
            new_y = (event.y - 50) // 100
            piece = self.get_piece_at(x, y)
            self.first_click = None
            
            self.game_state.board.move_piece(piece, new_x, new_y)
            self.update()

    def get_piece_at(self, x, y):
        """
        Returns the piece at a given position on the board.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        Returns:
            Piece: The piece at the given position, or None if there is no piece.
        """
        for piece in self.game_state.board:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    @staticmethod
    def __load_images():
        """Load images for each chess piece and return a dictionary mapping piece symbols to images."""
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
        """Draw the chess board on the canvas."""
        for i in range(8):
            for j in range(8):
                x1 = i * 100 + 50
                y1 = j * 100 + 50
                x2 = x1 + 100
                y2 = y1 + 100
                color = "#deb887" if (i + j) % 2 == 0 else "#4d3222"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_pieces(self):
        """Draw the chess pieces on the board."""
        board = self.game_state.board
        for piece in board:
            if piece is not None:
                x = (piece.x + 0.5) * 100 + 50
                y = (piece.y + 0.5) * 100 + 50
                image = self.images.get(piece.symbol)
                if image is not None:
                    self.canvas.create_image(x, y, image=image, anchor=tk.CENTER)

    def draw_labels(self):
        """Draw labels for the chess board."""
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
        """Update the chess board and pieces."""
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_labels()

    def run(self):
        """Start the Tkinter event loop."""
        self.update()
        self.root.mainloop()
