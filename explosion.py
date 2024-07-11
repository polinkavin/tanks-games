import pygame


# класс взрыв
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = (
            pygame.image.load('img/SplashLarge1.png'),
            pygame.image.load('img/SplashLarge2.png'),
            pygame.image.load('img/SplashLarge3.png'),
        )
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center  # (x, y)
        self.frame = 0
        self.frame_rate = 10
        self.last_update = pygame.time.get_ticks()  # ..:01

    def update(self, *args, **kwargs):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center=center)
