# Name: Chess Program
# Author: Eddie Elvira (@eelviral)
# Github_Page: https://www.github.com/eelviral/
# Created_On: Monday, March 7, 2022 at 05:51 UTC

import pygame

class Chess:
    def __init__(self):
        self.length = 500
        self.width = 500
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')

    def draw_board(self):
        '''
        Display black and white checkerboard background
        '''
        size = self.length / 8
        count = 0
        self.screen.fill(self.black)
        for i in range(self.length + 1):
            for j in range(self.length):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                                     size*j, size*i, size, size])
                count += 1
            count -= 1
        pygame.display.update()