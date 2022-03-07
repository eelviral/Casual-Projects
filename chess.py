# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC

from pieces import king
import pygame

class Chess:
    def __init__(self):
        self.length = 500
        self.width = 500
        self.bg_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')
        
        
    def run_game(self):
        # Variable to keep our game loop running
        running = True
        # game loop
        while running:
        # for loop through the event queue  
            for event in pygame.event.get():
                # Check for QUIT event      
                if event.type == pygame.QUIT:
                    running = False
        
if __name__ == '__main__':
    # King()
    # Queen()
    # Bishop()
    chess_game = Chess()
    chess_game.run_game()