import random

import pygame as p
from player import Player
from bullet import Bullet
from enemy import Enemy
from explosion import Explosion
from maps import Obstacle, Obstacle2
from powerup import PowerUp
from orel import Orel
import time

p.init()
p.mixer.init()

GAME_W = 800
GAME_H = 600

clock = p.time.Clock()
screen = p.display.set_mode((GAME_W, GAME_H))
p.display.set_caption('Tanks of world')
sound_1 = p.mixer.Sound('img/sfx/explosion-small.wav')
sound_1.set_volume(0.1)
sound_2 = p.mixer.Sound('img/sfx/bump.wav')
sound_2.set_volume(0.1)
sound_3 = p.mixer.Sound('img/sfx/shot.wav')
sound_3.set_volume(0.1)

# создаем группы для спрайтов
all_sprites = p.sprite.Group()
bots_group = p.sprite.Group()
bots_bullet_group = p.sprite.Group()
plr_bullet_group = p.sprite.Group()
orel_group = p.sprite.Group()
plr_group = p.sprite.Group()
power_group = p.sprite.Group()

plr = Player(200, 500)
plr_group.add(plr)


# Жизни игрока
def draw_lives(count):
    image = p.transform.scale(p.image.load('img/img_4.png'), (25, 25))
    image_rect = image.get_rect()
    image_rect.x = GAME_W // 2 + 100
    image_rect.y = GAME_H - 30
    for i in range(count):
        screen.blit(image, image_rect)
        image_rect.x += image.get_width() + 5


# меню
def menu():
    image = p.image.load('img/game.png')
    btn = p.image.load('img/BtnPlay.png')
    btn_rect = btn.get_rect()
    btn_rect.x = GAME_W // 2 - btn.get_width() // 2
    btn_rect.y = GAME_H // 2 - btn.get_height() // 2
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                quit()

        mouse_posX, mouse_posY = p.mouse.get_pos()
        mouse_click = p.mouse.get_pressed()

        # изменяем размер при наведении курсора на кнопку
        if btn_rect.collidepoint(mouse_posX, mouse_posY):
            btn_scale = p.transform.scale(btn, (btn.get_width() + 10, btn.get_height() + 10))
        else:
            btn_scale = p.transform.scale(btn, (btn.get_width(), btn.get_height()))
        btn_rect = btn_scale.get_rect()
        btn_rect.x = GAME_W // 2 - btn_scale.get_width() // 2
        btn_rect.y = GAME_H // 2 - btn_scale.get_height() // 2

        # клик по кнопке
        if btn_rect.collidepoint(mouse_posX, mouse_posY) and mouse_click[0] == True:
            return

        screen.blit(image, (0, 0))
        screen.blit(btn_scale, btn_rect)
        p.display.update()


menu()


# карты
def base():
    block = Obstacle(0, 0)
    block.rect.x = GAME_W // 2 - block.image.get_width() * 1.5
    block.rect.y = GAME_H - block.image.get_height()
    all_sprites.add(block)

    block = Obstacle(0, 0)
    block.rect.x = GAME_W // 2 - block.image.get_width() * 1.5
    block.rect.y = GAME_H - block.image.get_height() * 2
    all_sprites.add(block)

    block = Obstacle(0, 0)
    block.rect.x = GAME_W // 2 - block.image.get_width() // 2
    block.rect.y = GAME_H - block.image.get_height() * 2
    all_sprites.add(block)

    block = Obstacle(0, 0)
    block.rect.x = GAME_W // 2 + block.image.get_width() // 2
    block.rect.y = GAME_H - block.image.get_height() * 2
    all_sprites.add(block)

    block = Obstacle(0, 0)
    block.rect.x = GAME_W // 2 + block.image.get_width() // 2
    block.rect.y = GAME_H - block.image.get_height()
    all_sprites.add(block)

    # Орел
    orel = Orel(0, 0)
    orel.rect.x = GAME_W // 2 - orel.image.get_width() // 2
    orel.rect.y = GAME_H - orel.image.get_height()
    all_sprites.add(orel)
    orel_group.add(orel)


def map1():
    x = 73
    y = 55
    for _ in range(6):
        for i in range(8):
            block = Obstacle(x, y)
            all_sprites.add(block)
            y += block.image.get_height()
        x += 120
        y = 55


def map2():
    x = 73
    y = 100
    for _ in range(6):
        for i in range(4):
            block = Obstacle(x, y)
            all_sprites.add(block)
            y += block.image.get_height() * 2
        x += 120
        y = 100


def map3():
    x = 73
    y = 100
    a = 0
    for _ in range(2):
        for _ in range(3):
            for i in range(4):
                block = Obstacle(x, y)
                all_sprites.add(block)
                x += block.image.get_width()
            y += block.image.get_height() * 3
            x = 73 + a
        y = 100
        a += block.image.get_width() * 7
        x += a


def map4():
    x = 100
    y = 100
    block = Obstacle2(x, y)
    all_sprites.add(block)

    y += 45
    block = Obstacle2(155, 145)
    all_sprites.add(block)


def clearMap():
    all_sprites.empty()
    bots_bullet_group.empty()
    plr_bullet_group.empty()
    bots_group.empty()
    orel_group.empty()
    all_sprites.add(plr)


def start_game():
    current_map_index = 0
    clearMap()
    maps[current_map_index]()  # вызов первой функции из списка
    base()
    plr.lives = 3
    plr.rect.x = 200
    plr.rect.y = 500
    plr.new_angle = 0


# список карт
maps = [map1, map2, map3, map4]
current_map_index = 0
clearMap()
maps[current_map_index]()  # вызов первой функции из списка
base()
start_time = time.time()

# добавляем спрайты в группы
all_sprites.add(plr)

running = True
enemy_time = 30
bullet_time = 30
power_time = time.time()
stop_time = 90
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    # powerUps
    if time.time() - power_time > 10:
        pup = PowerUp()
        all_sprites.add(pup)
        power_group.add(pup)
        power_time = time.time()

    # смена карт
    if time.time() - start_time >= 30:  # 180 = 3 минуты
        current_map_index = (current_map_index + 1) % len(maps)
        clearMap()
        maps[current_map_index]()
        base()
        start_time = time.time()

    # перемещение игрока и границы
    keys = p.key.get_pressed()
    if keys[p.K_w]:
        plr.new_angle = 0
        if plr.rect.top > 0:
            plr.rect.y -= 5
    elif keys[p.K_d]:
        plr.new_angle = -90
        if plr.rect.right < GAME_W:
            plr.rect.x += 5
    elif keys[p.K_s]:
        plr.new_angle = 180
        if plr.rect.bottom < GAME_H:
            plr.rect.y += 5
    elif keys[p.K_a]:
        plr.new_angle = 90
        if plr.rect.left > 0:
            plr.rect.x -= 5

    # столкновения игрока с препятствиями
    hit = p.sprite.spritecollide(plr, all_sprites, False)
    for obs in hit:
        if isinstance(obs, Obstacle):
            # откатываем игрока
            if plr.new_angle == 0:
                plr.rect.y += 5
            elif plr.new_angle == -90:
                plr.rect.x -= 5
            elif plr.new_angle == 180:
                plr.rect.y -= 5
            elif plr.new_angle == 90:
                plr.rect.x += 5
            break

    # столкновения врагов с препятствиями
    for bot1 in bots_group:
        hit = p.sprite.spritecollide(bot1, all_sprites, False)
        for obs in hit:
            if isinstance(obs, Obstacle):
                # откатываем врага
                if bot1.angle == 0:
                    bot1.rect.y += 5
                elif bot1.angle == -90:
                    bot1.rect.x -= 5
                elif bot1.angle == 180:
                    bot1.rect.y -= 5
                elif bot1.angle == 90:
                    bot1.rect.x += 5
                bot1.rotate()
                break

    # стрельба игрока
    bullet_time -= 1
    mouse = p.mouse.get_pressed()  # (True, False, False)
    if mouse[0] and bullet_time <= 0:
        bullet = Bullet(plr.rect.center, plr.new_angle)
        plr_bullet_group.add(bullet)
        all_sprites.add(bullet)
        bullet_time = 10
        sound_3.play()

    # создание врагов
    enemy_time -= 1
    if enemy_time <= 0 and len(bots_group.sprites()) < 5 + current_map_index:
        bot = Enemy()
        bots_group.add(bot)
        all_sprites.add(bot)
        enemy_time = 30

    # стрельба врагов
    for current_bot in bots_group:
        if current_bot.shooting:
            bot_bullet = Bullet(current_bot.rect.center, current_bot.angle)
            bots_bullet_group.add(bot_bullet)
            all_sprites.add(bot_bullet)
            current_bot.shooting = False

    # столкновение врагов с пулями игрока
    for bul in plr_bullet_group:
        hit = p.sprite.spritecollide(bul, bots_group, True)  # [bul, bul]
        if hit:
            plr_bullet_group.remove(bul)
            all_sprites.remove(bul)
            for b in hit:
                all_sprites.remove(b)
                exp = Explosion(b.rect.center)
                all_sprites.add(exp)
                sound_1.play()

    # попадание врагов по игроку
    for bul in bots_bullet_group:
        hit = p.sprite.spritecollide(bul, plr_group, False)
        if hit:
            bots_bullet_group.remove(bul)
            all_sprites.remove(bul)
            plr.lives -= 1
            if plr.lives <= 0:
                menu()
                start_time = time.time()
                start_game()

    # столкновение пуль с препятствиями
    for bul in bots_bullet_group:
        hit = p.sprite.spritecollide(bul, all_sprites, False)
        for h in hit:
            if isinstance(h, Obstacle):
                h.live -= bul.damage
                bul.kill()
                sound_2.play()
            if isinstance(h, Orel):  # попадание в орла = game over
                bul.kill()
                menu()
                start_time = time.time()
                start_game()

    # столкновение пуль игрока с препятствиями
    for bul in plr_bullet_group:
        hit = p.sprite.spritecollide(bul, all_sprites, False)
        for h in hit:
            if isinstance(h, Obstacle):
                h.live -= bul.damage
                bul.kill()
                sound_2.play()
            if isinstance(h, Orel):  # попадание в орла = game over
                bul.kill()
                menu()
                start_time = time.time()
                start_game()

    # собираем powerUp
    hit = p.sprite.spritecollide(plr, power_group, True)
    for h in hit:
        if h.image_index == 0:
            for bot in bots_group:
                bot.speed = 0
                stop_time = 60
            plr.lives = 3
        if h.image_index == 2:
            base()

    stop_time -= 1
    if stop_time == 0:
        for bot in bots_group:
            bot.speed = 5

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    draw_lives(plr.lives)

    p.display.flip()
    clock.tick(20)
