import pygame
from chess import Chess

class Board(Chess):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((self.length, self.width))
        pygame.display.set_caption('Chess Game')

    def draw_board(self):
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
