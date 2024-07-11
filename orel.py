import pygame


class Orel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/Orel.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = 1
