import pygame
from board import Board
from itertools import product
import math

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {'white': {},
          'black': {}}
SQUARES = {i: None for i in list(product(range(8), range(8)))}


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
    board = Board()
    start = end = None
    moves_played = []

    def __init__(self):
        self.length = self.width = WIDTH
        self.black = (77, 50, 34)
        self.white = (222, 184, 135)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')
        self.board.reset_board()

    def player_move(self, start_x, start_y, end_x, end_y) -> bool:
        start_box = self.board.get_box(start_x, start_y)
        end_box = self.board.get_box(end_x, end_y)
        if start_box.piece is None:
            return False
        return start_box.piece.can_move(self.board, start_box, end_box)

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
                desc = str(box).split()
                if desc[0] == "None":
                    continue
                color, piece = [i.lower() for i in desc[:2]]
                row, col = [int(i) for i in desc[2:]]

                self.screen.blit(IMAGES[color][piece], (int(
                    col) * SQ_SIZE, int(row) * SQ_SIZE))
                SQUARES[(col, row)] = f'{color} {piece}'

    def mouse_click(self, pos):
        mouse_x, mouse_y = [math.floor(i / SQ_SIZE) for i in pos]

        if (mouse_x, mouse_y) in SQUARES.keys():
            if SQUARES[(mouse_x, mouse_y)] is not None:
                if self.start is not None:
                    self.end = None
                self.start = (mouse_x, mouse_y)
            else:
                if self.start is not None:
                    self.end = (mouse_x, mouse_y)

        if self.start is not None and self.end is not None:
            if self.player_move(self.start[1], self.start[0], self.end[1], self.end[0]):
                self.board.move_piece(
                    self.start[1], self.start[0], self.end[1], self.end[0])
                SQUARES[self.start] = None
            self.start = None
            self.end = None
