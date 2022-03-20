from board import Board
from game import Chess
import pygame

MAX_FPS = 15

if __name__ == '__main__':
    game = Chess()
    clock = pygame.time.Clock()
    IMAGES = game.load_images()
    
    running = True
    while running:
        pygame.time.delay(50)
        clock.tick(MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.draw_board()
