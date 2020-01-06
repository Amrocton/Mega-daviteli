import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((800, 300))
clock = pygame.time.Clock()


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


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 800 // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - 300 // 2)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                tiles_group.add(Tile('empty', x, y))
            elif level[y][x] == '#':
                tiles_group.add(Tile('wall', x, y))
                wall_group.add(Tile('wall', x, y))
            elif level[y][x] == '@':
                tiles_group.add(Tile('empty', x, y))
                new_player = Player(x, y)
                player_group.add(new_player)
    return new_player, x, y


def tor_move_y(sprite, height, width):
    if sprite.rect.y < 0:
        sprite.rect.y += height
    else:
        sprite.rect.y -= height
    if sprite.rect.x < 0:
        sprite.rect.x += width
    else:
        sprite.rect.x -= width


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Мар10", "",
                  "Правила игры:",
                  "По газону МОЖНО ходить",
                  "Коробки по два метра в высоту, навернёшься",
                  "Прежде чем начать, введите название уровня в консоли!!!"]

    fon = pygame.transform.scale(load_image('background.jpg'), (800, 300))
    screen.blit(fon, (0, 0))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

player, level_x, level_y = generate_level(load_level(input()))
camera = Camera()
back_surf = pygame.image.load('data/background.jpg')
back_rect = back_surf.get_rect(center=(400, 150))
screen.blit(back_surf, back_rect)
camera.update(player)
for sprite in all_sprites:
    camera.apply(sprite)
level_list = all_sprites.sprites()
check = True
while check:
    check = False
    if min(map(lambda sp: sp.rect.y, all_sprites.sprites())) > -50 and min(map(lambda sp: sp.rect.x, all_sprites.sprites())) > -50:
        check = True
        if min(map(lambda sp: sp.rect.y, all_sprites.sprites())) <= -50:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y -= 50 * max(map(lambda sp: sp.rect.x, all_sprites.sprites()))
                all_sprites.add(new_sprite)
        elif min(map(lambda sp: sp.rect.x, all_sprites.sprites())) <= -50:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y -= 50 * max(map(lambda sp: sp.rect.y, all_sprites.sprites()))
                all_sprites.add(new_sprite)
        else:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y -= 50 * max(map(lambda sp: sp.rect.y, all_sprites.sprites()))
                new_sprite.rect.y -= 50 * max(map(lambda sp: sp.rect.x, all_sprites.sprites()))
                all_sprites.add(new_sprite)
    if max(map(lambda sp: sp.rect.y, all_sprites.sprites())) < 300 and max(map(lambda sp: sp.rect.x, all_sprites.sprites())) < 800:
        check = True
        if max(map(lambda sp: sp.rect.y, all_sprites.sprites())) >= 300:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y += 50 * max(map(lambda sp: sp.rect.x, all_sprites.sprites()))
                all_sprites.add(new_sprite)
        elif max(map(lambda sp: sp.rect.x, all_sprites.sprites())) >= 800:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y += 50 * max(map(lambda sp: sp.rect.y, all_sprites.sprites()))
                all_sprites.add(new_sprite)
        else:
            for l_sprite in level_list:
                new_sprite = l_sprite.copy()
                new_sprite.rect.y += 50 * max(map(lambda sp: sp.rect.y, all_sprites.sprites()))
                new_sprite.rect.y += 50 * max(map(lambda sp: sp.rect.x, all_sprites.sprites()))
                all_sprites.add(new_sprite)
running = True
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 1)
go_up = go_down = go_left = go_right = False
while running:
    move = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                go_right = True
            elif event.key == pygame.K_LEFT:
                go_left = True
            elif event.key == pygame.K_UP:
                go_up = True
            elif event.key == pygame.K_DOWN:
                go_down = True
        if event.type == MYEVENTTYPE:
            move = 100 * clock.tick() // 1000
            pygame.time.set_timer(MYEVENTTYPE, 100)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                go_right = False
            elif event.key == pygame.K_LEFT:
                go_left = False
            elif event.key == pygame.K_UP:
                go_up = False
            elif event.key == pygame.K_DOWN:
                go_down = False
    if go_up or go_down or go_left or go_right:
        if go_up:
            player_group.sprites()[0].rect.y -= move
            if pygame.sprite.spritecollide(player, wall_group, False):
                player_group.sprites()[0].rect.y += move
        if go_down:
            player_group.sprites()[0].rect.y += move
            if pygame.sprite.spritecollide(player, wall_group, False):
                player_group.sprites()[0].rect.y -= move
        if go_left:
            player_group.sprites()[0].rect.x -= move
            if pygame.sprite.spritecollide(player, wall_group, False):
                player_group.sprites()[0].rect.x += move
        if go_right:
            player_group.sprites()[0].rect.x += move
            if pygame.sprite.spritecollide(player, wall_group, False):
                player_group.sprites()[0].rect.x -= move
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

    screen.blit(back_surf, back_rect)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
