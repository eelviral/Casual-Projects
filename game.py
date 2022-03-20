# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC

import pygame
from board import Board
from move import Move

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


class Game:
    player = [0] * 2
    board = Board()

    def initialize(self, p1, p2) -> None:
        self.players[0] = p1
        self.players[1] = p2

        self.board.reset_board()

        if p1.is_white_side():
            self.current_turn = p1
        else:
            self.current_turn = p2

        self.moves_played.clear()

    def is_end(self) -> bool:
        return self.get_status() != GameStatus.ACTIVE

    def get_status(self) -> bool:
        return self.status

    def set_status(self, status) -> None:
        self.status = status

    def player_move(self, player, start_x, start_y, end_x, end_y) -> bool:
        start_box = self.board.get_box(start_x, start_y)
        end_box = self.board.get_box(start_y, end_y)
        move = Move(player, start_box, end_box)
        return self.make_move(move, player)

    def make_move(move, player):
        source_piece = move.get_start()


class Chess:
    board = Board()
    
    def __init__(self):
        self.length = self.width = WIDTH
        self.black = (77, 50, 34)
        self.white = (222, 184, 135)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')

    @staticmethod
    def load_images() -> dict:
        wb_pieces = [['white', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']],
                     ['black', ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']]]
        for color, pieces in wb_pieces:
            for piece in pieces:
                IMAGES[color][piece] = pygame.transform.scale(
                    pygame.image.load(f'images/{color}/{piece}.png'),
                    (SQ_SIZE, SQ_SIZE))
        return IMAGES

    def draw_board(self) -> None:
        '''
        Display black and white checkerboard background
        '''
        size = SQ_SIZE
        count = 0
        self.screen.fill(self.black)
        for i in range(self.length + 1):
            for j in range(self.length):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                                     size*j, size*i, size, size])
                count += 1
            count -= 1
            
        self.board.reset_board()
        self.draw_pieces()
        pygame.display.update()

    def draw_pieces(self) -> None:
        boxes = self.board.boxes
        
        for box in boxes:
            for piece in box:
                desc = str(piece).split()
                if desc[0] == "None":
                    continue
                color, p, row, col = desc
                self.screen.blit(IMAGES[color.lower()][p.lower()], (int(col) * SQ_SIZE, int(row) * SQ_SIZE))
