import pygame
import os
import random
import sys

pygame.init()


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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = random.choice(tile_images[tile_type])
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(tile_w * pos_x, tile_h * pos_y)


class Player()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
land_group = pygame.sprite.Group()
players_group = pygame.sprite.Group()
