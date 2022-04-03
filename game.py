import pygame
from board import Board
from move import Move
from pieces.king import King
import math

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {'white': {},
          'black': {}}


class GameStatus:
    ACTIVE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    FORFEIT = 3
    STALEMATE = 4
    RESIGNATION = 5


class Highlight:
    def __init__(self, x, y, color=(227, 227, 118)):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x*SQ_SIZE,
                                              self.y*SQ_SIZE, SQ_SIZE, SQ_SIZE))


class Game:
    players = []
    board = Board()
    current_turn = None
    move = []
    highlighted_boxes = []
    moves_played = []

    def __init__(self):
        self.length = self.width = WIDTH
        self.black = (77, 50, 34)
        self.white = (222, 184, 135)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')
        self.load_images()
        self._status = None

    def init(self, p1, p2):
        if len(self.players) == 0:
            self.players.append(p1)
            self.players.append(p2)
        else:
            self.players[0] = p1
            self.players[1] = p2

        self.board.reset_board()

        if p1.is_white_side:
            self.current_turn = p1
        else:
            self.current_turn = p2

        self.moves_played.clear()

    @property
    def status(self) -> bool:
        """Get or set the GameStatus

        Returns: bool
        """
        return self._status

    @status.setter
    def status(self, value) -> None:
        self._status = value

    def player_move(self, player, start_x, start_y, end_x, end_y) -> bool:
        start_box = self.board.get_box(start_x, start_y)
        if start_box.piece is None:
            return False

        end_box = self.board.get_box(end_x, end_y)
        move = Move(player, start_box, end_box)
        return self.make_move(move, player)

    def make_move(self, move, player) -> bool:
        start_piece = move.start.piece

        # Cannot move an empty box
        if start_piece is None:
            return False

        # Check if its player's turn
        if player != self.current_turn:
            return False
        if start_piece.is_white != player.is_white_side:
            return False

        # Check if piece can make this move
        if not start_piece.can_move(self.board, move.start, move.end):
            return False

        # Check if a piece is getting captured
        end_piece = move.end.piece
        if end_piece is not None:
            end_piece.captured = True
            move.piece_captured = end_piece

        # Check if a castling move is occurring
        if (start_piece is not None and isinstance(start_piece, King)
                and start_piece.is_castling):
            move.castling_move = True

        # Keep track of move
        self.moves_played.append(str(move))

        # Move the piece
        move.end.piece = move.start.piece
        move.start.piece = None

        # Game ends when King is under attack
        if end_piece is not None and isinstance(end_piece, King):
            if player.is_white_side:
                self.status = GameStatus.WHITE_WIN
            else:
                self.status = GameStatus.BLACK_WIN

        # Let other player move next turn
        if self.current_turn == self.players[0]:
            self.current_turn = self.players[1]
        else:
            self.current_turn = self.players[0]
        return True

    @staticmethod
    def load_images() -> None:
        wb_pieces = [['white', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']],
                     ['black', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']]]
        for color, pieces in wb_pieces:
            for piece in pieces:
                IMAGES[color][piece] = pygame.transform.scale(
                    pygame.image.load(f'images/{color}/{piece}.png'),
                    (SQ_SIZE, SQ_SIZE))

    def draw_board(self) -> None:
        """
        Display black and white checkerboard background
        """
        size = SQ_SIZE
        count = 0
        self.screen.fill(self.black)
        for i in range(self.length + 1):
            for j in range(self.length):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                        size * j, size * i, size, size])
                count += 1
            count -= 1

        # Add highlighted box
        if len(self.highlighted_boxes) > 0:
            for box in self.highlighted_boxes:
                box.draw(self.screen)

        self.draw_pieces()
        pygame.display.update()

    def draw_pieces(self) -> None:
        boxes = self.board.boxes

        for row in boxes:
            for box in row:
                if box.piece is None:
                    continue

                color, piece = [i.lower() for i in str(box.piece).split()]
                if box.piece.is_white:
                    self.screen.blit(IMAGES[color][piece],
                                     (int(box.y) * SQ_SIZE, int(box.x) * SQ_SIZE))
                else:
                    self.screen.blit(IMAGES[color][piece],
                                     (int(box.y) * SQ_SIZE, int(box.x) * SQ_SIZE))

    def mouse_click(self, pos) -> None:
        mouse_x, mouse_y = [math.floor(i / SQ_SIZE) for i in pos]
        selected_piece = self.board.get_box(mouse_y, mouse_x).piece
        if len(self.highlighted_boxes) >= 2:
            self.highlighted_boxes.clear()

        # If a start piece has not been chosen
        if len(self.move) == 0:
            # Add start piece to move data if spot is not empty
            if selected_piece is not None:
                self.move.append((mouse_x, mouse_y))
                self.highlighted_boxes.append(Highlight(mouse_x, mouse_y))
        # If a start piece has been chosen
        elif len(self.move) == 1:
            # Switch chosen start piece if player picks piece of same color
            if selected_piece is not None and selected_piece.is_white == self.board.get_box(self.move[0][0], self.move[0][1]).piece:
                self.move[0] = (mouse_x, mouse_y)
                self.highlighted_boxes[0] = Highlight(mouse_x, mouse_y)
            # Add end position to move data if spot is empty or has opposite color piece
            else:
                self.move.append((mouse_x, mouse_y))
                self.highlighted_boxes.append(Highlight(mouse_x, mouse_y))

        # If both a start and end piece have been chosen
        if len(self.move) == 2:
            # Check if the move is playable
            if self.player_move(self.current_turn, self.move[0][1],
                                self.move[0][0], self.move[1][1], self.move[1][0]):
                print(self.moves_played[-1])
                self.highlighted_boxes.append(Highlight(self.move[1][0], self.move[1][1]))
            else:
                self.highlighted_boxes.clear()
            # Clear move data
            self.move.clear()
