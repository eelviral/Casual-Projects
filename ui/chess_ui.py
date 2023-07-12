import tkinter as tk
from engine.chess_game import ChessGame
from pieces import Piece
from ui.click_handler import ClickHandler

WHITE_IMAGES = 'images/white/'
BLACK_IMAGES = 'images/black/'
SCREEN_WIDTH = 900


class ChessUI:
    """
    This class creates and manages the graphical user interface for a chess game. It includes
    functionality to draw the game board, game pieces, and handle user interaction.

    Attributes:
        game (ChessGame): The chess game to use.
        root (Tk): The root Tkinter instance.
        canvas (Canvas): The Tkinter canvas to draw the game on.
        images (dict): Dictionary mapping piece symbols to their corresponding image files.
        first_click (tuple): The coordinates of the first click, or None if no click has been made yet.
        selected_piece (Piece): The currently selected chess piece, or None if no piece is selected.
        legal_moves (list): List of all current legal moves.
        click_handler (ClickHandler): Instance of the click handler to manage click events.
    """

    def __init__(self, chess_game: ChessGame):
        """
        Initializes the ChessUI with a given chess game, sets up the game window,
        and binds mouse click events to the click handler.

        Args:
            chess_game (ChessGame): The chess game being played.
        """
        self.game = chess_game

        # Initialize screen
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_WIDTH)
        self.canvas.pack()

        # Set the window icon and title
        self.root.iconbitmap('images/ico/chess-icon.ico')
        self.root.title("Chess")

        # Center the canvas
        self.center_canvas()

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
        Calculates the legal moves for a given piece and updates the game board accordingly.

        Args:
            piece (Piece): The chess piece to calculate legal moves for.
        """
        self.legal_moves = self.game.move_generator.piece_legal_moves(piece)
        self.update()  # Update immediately after calculating legal moves

    @staticmethod
    def __load_images() -> dict:
        """
        Load images for each black and white chess piece.

        Returns:
            dict: A dictionary mapping piece symbols to their respective image files.
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
        """
        Draws the chess board on the canvas, alternating the square colors.
        If there are any legal moves for a selected piece, the squares of these moves are highlighted green.
        """
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
        """
        Iterates through all chess pieces on the game board and draws them on the canvas at their respective locations.
        """
        for piece in self.game.board:
            if piece is not None:
                x = (piece.x + 0.5) * 100 + 50
                y = (piece.y + 0.5) * 100 + 50
                image = self.images.get(piece.symbol)
                if image is not None:
                    self.canvas.create_image(x, y, image=image, anchor=tk.CENTER)

    def draw_labels(self):
        """
        Draws labels for the chess board columns (A-H) and rows (1-8) on the canvas.
        """
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

    def center_canvas(self):
        """
        Centers the game window on the screen, accounting for screen resolution.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Positioning the window in the center of the screen
        x_coordinate = (screen_width / 2) - (SCREEN_WIDTH / 2)
        y_coordinate = (screen_height / 2) - (SCREEN_WIDTH / 1.95)

        self.root.geometry("%dx%d+%d+%d" % (SCREEN_WIDTH, SCREEN_WIDTH, x_coordinate, y_coordinate))

    def update(self):
        """
        Updates the chess board and pieces by deleting all canvas content and redrawing the board,
        pieces, and labels.
        """
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_labels()

    def run(self):
        """
        Starts the Tkinter event loop, which waits for user interaction until the game window is closed.
        """
        self.update()
        self.root.mainloop()
