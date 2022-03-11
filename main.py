from game import Chess
from board import Board
import pygame

if __name__ == '__main__':
    game = Chess()
    board = Board()
    # clock = pygame.time.Clock()

    board.reset_board()
    running = True
    while running:
        # pygame.time.delay(30)
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.draw_board()
