# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC

from game import Game, GameStatus
from player import Human, Computer
from ai import find_random_move
import pygame

MAX_FPS = 15

if __name__ == '__main__':
    pygame.init()

    game = Game()
    white = Human(white_side=True)
    black = Computer(white_side=False)
    game.init(black, white)

    running = True
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    while running:
        pygame.time.delay(50)
        clock.tick(MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and isinstance(game.current_turn, Human):
                game.mouse_click(event.pos)
            if event.type == pygame.USEREVENT and isinstance(game.current_turn, Computer):
                legal_moves = game.get_current_legal_moves()
                computer_move = find_random_move(legal_moves)
                game.move_action(computer_move[0][1], computer_move[0][0])
                game.move_action(computer_move[1][1], computer_move[1][0])
        game.draw_board()

        if game.status != GameStatus.ACTIVE:
            if game.status == GameStatus.BLACK_WIN:
                print("Black Wins!")
            elif game.status == GameStatus.WHITE_WIN:
                print("White Wins!")
            elif game.status == GameStatus.STALEMATE:
                print("Stalemate!")
            running = False
