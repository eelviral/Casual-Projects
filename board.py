import pygame
from chess import Chess


class Board(Chess):
    def __init__(self):
        super().__init__()

    def draw_board(self):
        size = 20
        count = 0
        for i in range(1, self.length + 1):
            for j in range(1, self.length + 1):
                if count % 2 == 0:
                    pygame.draw.rect(self.screen, self.white, [
                                     size*j, size*i, size, size])
                else:
                    pygame.draw.rect(self.screen, self.black, [
                                     size*j, size*i, size, size])
                count += 1
            count -= 1
        pygame.display.update()
