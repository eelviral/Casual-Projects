from chess import Chess
from board import Board
import pygame

if __name__ == '__main__':
    chess_game = Chess()
    board = Board()

    # clock = pygame.time.Clock()

    running = True
    while running:
        # pygame.time.delay(30)
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        board.draw_board()
    