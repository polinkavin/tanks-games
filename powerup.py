import time

import pygame
import random


# класс взрыв
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = (
            pygame.image.load('img/img_1.png'),
            pygame.image.load('img/img_2.png'),
            pygame.image.load('img/img_3.png'),
        )
        self.image_index = random.randint(0, 2)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800 - self.image.get_width())
        self.rect.y = random.randint(0, 600 - self.image.get_height())
        self.lifetime = 20
        self.createtime = time.time()

    def update(self, *args, **kwargs):
        if time.time() - self.createtime > self.lifetime:
            self.kill()
