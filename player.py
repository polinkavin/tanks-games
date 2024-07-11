import pygame as p
from tanktools import getRotatedImage


class Player(p.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = p.image.load('img/Tank.png')
        self.image = p.image.load('img/Tank.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0  # текущий угол танка
        self.new_angle = 0  # новый угол танка
        self.lives = 3

    def update(self, *args, **kwargs):
        # поворот танка
        if self.new_angle != self.angle:
            self.angle = self.new_angle
            self.image, self.rect = getRotatedImage(self.original_image, self.rect, self.angle)

