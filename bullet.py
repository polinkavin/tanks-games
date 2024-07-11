import pygame as p
from tanktools import getRotatedImage


class Bullet(p.sprite.Sprite):
    def __init__(self, center, angle):
        super().__init__()
        self.angle = angle
        self.speed = 30
        self.image = p.image.load('img/img.png')
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image, self.rect = getRotatedImage(self.image, self.rect, angle)
        self.damage = 1

    def update(self, *args, **kwargs):
        if self.angle == 0:
            self.rect.x += 0
            self.rect.y -= self.speed
        elif self.angle == 90:
            self.rect.x -= self.speed
            self.rect.y -= 0
        elif self.angle == -90:
            self.rect.x += self.speed
            self.rect.y -= 0
        elif self.angle == 180:
            self.rect.x -= 0
            self.rect.y += self.speed


