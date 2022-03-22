from board import Board
from game import Game
import pygame

MAX_FPS = 15

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.load_images()
    
    running = True
    clock = pygame.time.Clock()
    while running:
        pygame.time.delay(50)
        clock.tick(MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.mouse_click(event.pos)
                # check_mouse_click(event.pos)
        game.draw_board()
