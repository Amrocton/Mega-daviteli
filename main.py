import pygame
import os
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
levelnum = random.randint(1, 4)
levelnum = 1
back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
back_rect = back_surf.get_rect(center=(400, 250))
screen.blit(back_surf, back_rect)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_level(filename):
    filename = "data/levels/" + filename + '.txt'
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'land': [load_image('level_atr/platform1.png'), load_image('level_atr/platform2.png')],
    'empty': [load_image('level_atr/void1.png'), load_image('level_atr/void2.png'),
              load_image('level_atr/void3.png')]}

tile_w = 80
tile_h = 50
velocity = list(
    [-75.0, -70, -65.0, -60, -55.0, -50, -45.0, -40, -35.0, -30, -25.0, -20, -15.0, -10, -5.0, 0,
     5.0, 10, 15.0, 20, 25.0, 30, 35.0, 40, 45.0, 50, 55.0, 60, 65.0, 70, 75.0]
    )


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = random.choice(tile_images[tile_type])
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(tile_w * pos_x, tile_h * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, lp, color, spawn_points, first_spawn):
        super().__init__(player_group, all_sprites)
        self.lifes = lp
        self.image = load_image(f'Gnomes/{color}/idle-0.png')  # !!!тут должна быть анимация!!!
        self.rect = self.image.get_rect()
        self.rect.x = first_spawn[0]
        self.rect.y = first_spawn[1]


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
land_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sg_red = pygame.sprite.Group()
sg_green = pygame.sprite.Group()
sg_blue = pygame.sprite.Group()
sg_yellow = pygame.sprite.Group()


def generate_level(level):
    spawn_coords = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                tiles_group.add(Tile('empty', x, y))
            elif level[y][x] == '#':
                tiles_group.add(Tile('land', x, y))
                land_group.add(Tile('land', x, y))
            elif level[y][x] == '@':
                spawn_coords.append((tile_w * x, tile_h * y))
    return spawn_coords


FPS = 30


def start_screen(screen):
    intro_text = ["Мар10", "",
                  "Правила игры:",
                  "По газону МОЖНО ходить",
                  "Коробки по два метра в высоту, навернёшься",
                  "Прежде чем начать, введите название уровня в консоли!!!"]
    screen.fill(pygame.Color('darkseagreen'))
    screen.blit(back_surf, back_rect)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    unstart = True
    while unstart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                unstart = False
        pygame.display.flip()
        clock.tick(FPS)
    game_start(screen)


def game_start(screen):
    lp = 3
    while True:
        screen.fill((0, 0, 0))
        back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
        back_rect = back_surf.get_rect(center=(400, 250))
        screen.blit(back_surf, back_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def game_loop(screen, playersnum, lp):
    spawn_points = generate_level(load_level(str(levelnum)))
    first_spawn = spawn_points.copy()
    random.shuffle(first_spawn)
    if playersnum >= 1:
        red_gnome = Player(lp, 'red', spawn_points, first_spawn.pop(0))
    if playersnum >= 2:
        green_gnome = Player(lp, 'green', spawn_points, first_spawn.pop(0))
    if playersnum >= 3:
        blue_gnome = Player(lp, 'blue', spawn_points, first_spawn.pop(0))
    if playersnum == 4:
        yellow_gnome = Player(lp, 'yellow', spawn_points, first_spawn.pop(0))

    while True:
        back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
        back_rect = back_surf.get_rect(center=(400, 250))
        screen.blit(back_surf, back_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


game_loop(screen, 2, 3)
