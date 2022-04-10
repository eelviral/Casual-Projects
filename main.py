# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC

from game import Game, GameStatus
from player import Human
import pygame

MAX_FPS = 15

if __name__ == '__main__':
    pygame.init()

    game = Game()
    white = Human(True)
    black = Human(False)
    game.init(black, white)

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
        game.draw_board()

        if game.status == GameStatus.BLACK_WIN:
            print("Black Wins!")
            running = False
        elif game.status == GameStatus.WHITE_WIN:
            print("White Wins!")
            running = False
