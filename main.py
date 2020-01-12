import pygame
import os
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
levelnum = random.randint(1, 2)
back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
back_rect = back_surf.get_rect(center=(400, 250))
screen.blit(back_surf, back_rect)
# вверх-влево-вправо-вниз
move_keys = {'red': [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s],
             'green': [pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k]}


def obj_upper(faller, x1, y1, w1, h1, x2, y2, w2, h2):
    return y2 <= y1 + h1 <= y2 + h2 and (
                x2 <= x1 <= x2 + w2 or x2 <= x1 + w1 <= x2 + w2) or faller.falling


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
    [-20.5, -19, -18.5, -17.5, -17, -16.5, -16, -15.5, -15, -14.5, -14, -13.5, -13, -12.5, 8, -5, -3,
     -2, -1, 0, 1, 2, 3, 5, 8, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18.5, 19,
     20.5]
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
        self.go_down = False
        self.dead = False
        self.spawn_points = spawn_points
        self.jumping = False
        self.falling = True
        self.velocity_index = 0
        self.move_left = False
        self.move_right = False
        self.image = load_image(f'Gnomes/{color}/idle-0.png')  # !!!тут должна быть анимация!!!
        self.rect = self.image.get_rect()
        self.rect.x = first_spawn[0]
        self.rect.y = first_spawn[1]
        self.move_key = move_keys[color]

    def rebirth(self):
        if self.lifes != 0:
            self.lifes -= 1
            self.jumping = False
            self.falling = True
            self.velocity_index = 0
            self.move_left = False
            self.move_right = False
            spawn = random.choice(self.spawn_points)
            self.rect.x = spawn[0]
            self.rect.y = spawn[1]
        else:
            self.dead = True

    def on_land(self):
        if pygame.sprite.spritecollideany(self, land_group):
            land = pygame.sprite.spritecollideany(self, land_group)
            if obj_upper(self, self.rect.x, self.rect.y, 30, 30, land.rect.x, land.rect.y, 80, 50):
                self.rect.y = land.rect.y - 29
                self.jumping = False
                self.falling = False
                self.velocity_index = 0
        elif not self.jumping:
            self.jumping = True
            self.falling = True
            self.velocity_index = 20

    def do_jumping(self):
        global velocity
        if self.jumping:
            self.rect.y += velocity[self.velocity_index]
            self.velocity_index += 1
            if self.velocity_index >= len(velocity) - 1:
                self.velocity_index = len(velocity) - 1
            if self.velocity_index >= 20:
                self.falling = True

    def move(self):
        x, y = self.rect.x, self.rect.y
        if self.move_left:
            self.rect.x -= 5
        if self.move_right:
            self.rect.x += 5
        self.do_jumping()
        if self.go_down:
            self.rect.y += 80
            self.go_down = False
        if pygame.sprite.spritecollideany(self, land_group):
            land = pygame.sprite.spritecollideany(self, land_group)
            if not obj_upper(self, self.rect.x, self.rect.y, 30, 30, land.rect.x, land.rect.y, 80,
                             50) and self.falling:
                self.rect.x, self.rect.y = x, y
        if self.rect.y > 510:
            self.rebirth()


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


FPS = 60


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
        back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
        back_rect = back_surf.get_rect(center=(400, 250))
        screen.blit(back_surf, back_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()


def game_loop(screen, playersnum, lp):
    clock = pygame.time.Clock()
    spawn_points = generate_level(load_level(str(levelnum)))
    first_spawn = spawn_points.copy()
    random.shuffle(first_spawn)
    blue_gnome, yellow_gnome, gnomes = None, None, []
    red_gnome = Player(lp, 'red', spawn_points, first_spawn.pop(0))
    green_gnome = Player(lp, 'green', spawn_points, first_spawn.pop(0))
    gnomes.extend([red_gnome, green_gnome])
    if playersnum >= 3:
        blue_gnome = Player(lp, 'blue', spawn_points, first_spawn.pop(0))
        gnomes.append(blue_gnome)
    if playersnum == 4:
        yellow_gnome = Player(lp, 'yellow', spawn_points, first_spawn.pop(0))
        gnomes.append(yellow_gnome)
    back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
    back_rect = back_surf.get_rect(center=(400, 250))
    while True:
        screen.blit(back_surf, back_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == red_gnome.move_key[0] and red_gnome.jumping is False:
                    red_gnome.jumping = True
                if event.key == green_gnome.move_key[0] and green_gnome.jumping is False:
                    green_gnome.jumping = True
                if blue_gnome:
                    if event.key == blue_gnome.move_key[0] and blue_gnome.jumping is False:
                        blue_gnome.jumping = True
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[0] and yellow_gnome.jumping is False:
                        yellow_gnome.jumping = True
                if event.key == red_gnome.move_key[1]:
                    red_gnome.move_left = True
                if event.key == green_gnome.move_key[1]:
                    green_gnome.move_left = True
                if blue_gnome:
                    if event.key == blue_gnome.move_key[1]:
                        blue_gnome.move_left = True
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[1]:
                        yellow_gnome.move_left = True
                if event.key == red_gnome.move_key[2]:
                    red_gnome.move_right = True
                if event.key == green_gnome.move_key[2]:
                    green_gnome.move_right = True
                if blue_gnome:
                    if event.key == blue_gnome.move_key[2]:
                        blue_gnome.move_right = True
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[2]:
                        yellow_gnome.move_right = True
                if event.key == red_gnome.move_key[3]:
                    red_gnome.go_down = True
                if event.key == green_gnome.move_key[3]:
                    green_gnome.go_down = True
                if blue_gnome:
                    if event.key == blue_gnome.move_key[3]:
                        blue_gnome.go_down = True
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[3]:
                        yellow_gnome.go_down = True
            if event.type == pygame.KEYUP:
                if event.key == red_gnome.move_key[1]:
                    red_gnome.move_left = False
                if event.key == green_gnome.move_key[1]:
                    green_gnome.move_left = False
                if blue_gnome:
                    if event.key == blue_gnome.move_key[1]:
                        blue_gnome.move_left = False
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[1]:
                        yellow_gnome.move_left = False
                if event.key == red_gnome.move_key[2]:
                    red_gnome.move_right = False
                if event.key == green_gnome.move_key[2]:
                    green_gnome.move_right = False
                if blue_gnome:
                    if event.key == blue_gnome.move_key[2]:
                        blue_gnome.move_right = False
                if yellow_gnome:
                    if event.key == yellow_gnome.move_key[2]:
                        yellow_gnome.move_right = False

        for gnome in gnomes:
            gnome.move()
            gnome.on_land()
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


game_loop(screen, 2, 3)
