import pkgutil

import pygame

pygame.mixer.init()
sound_1 = pygame.mixer.Sound('img/sfx/break.wav')
sound_1.set_volume(0.1)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/abstacle2.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = 5

    def update(self, *args, **kwargs):
        if self.live <= 0:
            self.kill()
            sound_1.play()


class Obstacle2(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('img/abstacle1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = 10
