import pygame
from random import randint, choice
from tanktools import getRotatedImage

GAME_W = 800
GAME_H = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if randint(1, 2) == 1:
            self.image = pygame.image.load('img/Tank2.png')
            self.original_image = pygame.image.load('img/Tank2.png')
        else:
            self.image = pygame.image.load('img/Tank3.png')
            self.original_image = pygame.image.load('img/Tank3.png')
        self.rect = self.image.get_rect()
        self.rect.y = 0

        if randint(1, 2) == 1:
            self.rect.x = 0
            self.angle = choice((-90, 180))
        else:
            self.rect.x = GAME_W - self.image.get_width()
            self.angle = choice((90, 180))

        self.image, self.rect = getRotatedImage(self.image, self.rect, self.angle)

        self.move_time = randint(60, 150)  # время движения
        self.time_count = 0  # счетчик времени
        self.speed = 5
        self.shoot_time = 30  # счетчик времени стрельбы
        self.shooting = False

    def update(self, *args, **kwargs):
        if self.speed > 0:
            # движение танка
            match self.angle:
                case 0:
                    self.rect.y -= self.speed
                case 90:
                    self.rect.x -= self.speed
                case 180:
                    self.rect.y += self.speed
                case -90:
                    self.rect.x += self.speed

            # проверка таймера стрельбы
            self.shoot_time -= 1
            if self.shoot_time <= 0:
                self.shooting = True
                self.shoot_time = 30

            # проверка таймера поворота
            self.time_count += 1
            if self.time_count >= self.move_time:
                self.rotate()
                self.time_count = 0
                self.move_time = randint(60, 150)

            # границы игры
            if self.rect.left < 0:
                self.rect.left = 0
                self.rotate()
            if self.rect.right > GAME_W:
                self.rect.right = GAME_W
                self.rotate()
            if self.rect.top < 0:
                self.rect.top = 0
                self.rotate()
            if self.rect.bottom > GAME_H:
                self.rect.bottom = GAME_H
                self.rotate()

    #  поворот танка
    def rotate(self):
        self.angle = choice((-90, 0, 180, 90))
        self.image, self.rect = getRotatedImage(self.original_image, self.rect, self.angle)
