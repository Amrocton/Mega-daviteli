import pygame
import os
import random
import sys
from GIFImage import GIFImage

gnomes = []
is_start = False
paused = False
lp = 3
GRAVITY = 2
playersnum = 2
pygame.init()
screen = pygame.display.set_mode((800, 500), pygame.FULLSCREEN)
clock = pygame.time.Clock()
back_surf = pygame.image.load(f'data/background{2}.jpg')
back_rect = back_surf.get_rect(center=(400, 250))
levelnum = random.randint(1, 4)
# вверх-влево-вправо-вниз
move_keys = {'red': [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s],
             'green': [pygame.K_p, pygame.K_l, 39, 59],
             'blue': [pygame.K_y, pygame.K_g, pygame.K_j, pygame.K_h],
             'yellow': [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]}
hit_sound = pygame.mixer.Sound('data/sound/Hit.wav')
select_sound = pygame.mixer.Sound('data/sound/Select.wav')
press_sound = pygame.mixer.Sound('data/sound/Press.wav')


def starting():
    global is_start
    is_start = True


def to_intro():
    start_screen(screen)


def to_menu():
    all_sprites.empty()
    land_group.empty()
    player_group.empty()
    tiles_group.empty()
    game_start(screen)



def secret():
    chika = GIFImage('data/scd.gif')
    pygame.mixer.music.load('data/sound/scd.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())

        all_particles.update()
        screen.fill((0, 0, 0))
        chika.render(screen, (0, 0))
        all_particles.draw(screen)
        pygame.display.flip()
        clock.tick(50)
    terminate()


def unpause():
    global paused
    paused = False
    pygame.mixer.music.load('data/sound/Kirby.mp3')
    pygame.mixer.music.play(-1)


def restart():
    all_sprites.empty()
    land_group.empty()
    player_group.empty()
    tiles_group.empty()
    game_loop(screen)


def players_change():
    global playersnum
    playersnum = (playersnum + 1) % 5
    if playersnum == 0:
        playersnum = 2


def lifes_change_add():
    global lp
    lp += 1
    if lp > 15:
        lp = 15


def lifes_change_add():
    global lp
    lp -= 1
    if lp < 1:
        lp = 1


def lifes_change_drop():
    global lp
    lp = 3


def obj_upper(faller, x1, y1, w1, h1, x2, y2, w2, h2):
    return y2 <= y1 + h1 <= y2 + h2 and (
            x2 <= x1 <= x2 + w2 or x2 <= x1 + w1 <= x2 + w2) or faller.falling


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        # pygame.mixer.Sound.play(select_sound)!!!fix!!!
        if click[0] == 1 and action is not None:
            if not button.is_clicked:
                pygame.mixer.Sound.play(press_sound)
                action()
                button.is_clicked = True
        else:
            button.is_clicked = False
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font('data/17990.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


button.is_clicked = False


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
    [-20.5, -19, -18.5, -17.5, -17, -16.5, -16, -15.5, -15, -14.5, -14, -13.5, -13, -12.5, -8, -5,
     -3,
     -2, -1, 0, 1, 2, 3, 5, 8, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18.5, 19,
     20.5]
)
screen_rect = (0, 0, 800, 500)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("heart.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_particles)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


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
        self.lifes -= 1
        if self.lifes != 0:
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

    def move(self, gnomes):
        if self.jumping or self.falling:
            speed = 4
        else:
            speed = 8
        x, y = self.rect.x, self.rect.y
        if self.move_left:
            self.rect.x -= speed
        if self.move_right:
            self.rect.x += speed
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
        for other in gnomes:
            if pygame.sprite.collide_rect(self, other) and self != other:
                if self.falling:
                    if other.rect.y > self.rect.y:
                        other.rebirth()
                        self.velocity_index = 13
                        pygame.mixer.Sound.play(hit_sound)
                elif obj_upper(self, self.rect.x, self.rect.y, 30, 30, other.rect.x, other.rect.y,
                               30, 30):
                    self.rect.y = other.rect.y - 29
                    self.jumping = False
                self.rect.x, self.rect.y = x, y


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

all_particles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
land_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sg_red = pygame.sprite.Group()
sg_green = pygame.sprite.Group()
sg_blue = pygame.sprite.Group()
sg_yellow = pygame.sprite.Group()
gnome_list = [sg_red, sg_green, sg_blue, sg_yellow]


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
    pygame.mixer.music.load('data/sound/Intro.mp3')
    pygame.mixer.music.play()
    intro_text = ["MEGA", "                  DAVITELI!!!",
                  "Правила игры:",
                  "Прыгай противнику на голову!",
                  "Но будь осторожен:",
                  "Тебя могут втоптать тоже!!!",
                  'Последний игрок победил!!!']
    screen.fill(pygame.Color('darkseagreen'))
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
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('data/sound/Intro_loop.mp3')
            pygame.mixer.music.play(-1)
        pygame.display.flip()
        clock.tick(FPS)
    game_start(screen)


def game_start(screen):
    global is_start, lp, playersnum
    is_start = False
    pygame.mixer.music.load('data/sound/Menu.mp3')
    pygame.mixer.music.play(-1)
    while not is_start:
        back_surf = pygame.image.load(f'data/background{levelnum}.jpg')
        back_rect = back_surf.get_rect(center=(400, 250))
        dim_screen = pygame.Surface(screen.get_size()).convert_alpha()
        dim_screen.fill((0, 0, 0, 180))
        screen.blit(back_surf, back_rect)
        screen.blit(dim_screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        button('Start the game!', 300, 100, 150, 50, (245, 245, 220), (145, 145, 120), starting)
        button(f'Players:{playersnum}', 300, 200, 80, 40, (245, 245, 220), (145, 145, 120),
               players_change)
        button(f'Lifes:{lp}', 420, 200, 80, 40, (245, 245, 220), (145, 145, 120), lifes_change_drop)
        button('Quit to intro', 300, 300, 150, 50, (245, 245, 220), (145, 145, 120), to_intro)
        button('Quit the game', 300, 400, 150, 50, (245, 245, 220), (145, 145, 120), terminate)
        button('Secret', 780, 480, 20, 20, (245, 245, 220), (145, 145, 120), secret)
        pygame.display.flip()
    game_loop(screen)


def game_loop(screen):
    global paused, lp, playersnum
    levelnum = random.randint(1, 4)
    paused = False
    pygame.mixer.music.load('data/sound/Kirby.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    spawn_points = generate_level(load_level(str(levelnum)))
    first_spawn = spawn_points.copy()
    random.shuffle(first_spawn)
    dim_screen = pygame.Surface(screen.get_size()).convert_alpha()
    dim_screen.fill((0, 0, 0, 180))
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
                if event.key == 27:
                    if paused:
                        unpause()
                    else:
                        paused = True
                        pygame.mixer.music.load('data/sound/Pause.mp3')
                        pygame.mixer.music.play(-1)
                if not paused:
                    if event.key == red_gnome.move_key[0] and red_gnome.jumping is False:
                        red_gnome.jumping = True
                        pygame.mixer.Sound.play(
                            pygame.mixer.Sound(f'data/sound/Jump{random.randint(1, 4)}.wav'))
                    if event.key == green_gnome.move_key[0] and green_gnome.jumping is False:
                        green_gnome.jumping = True
                        pygame.mixer.Sound.play(
                            pygame.mixer.Sound(f'data/sound/Jump{random.randint(1, 4)}.wav'))
                    if blue_gnome:
                        if event.key == blue_gnome.move_key[0] and blue_gnome.jumping is False:
                            blue_gnome.jumping = True
                            pygame.mixer.Sound.play(
                                pygame.mixer.Sound(f'data/sound/Jump{random.randint(1, 4)}.wav'))
                    if yellow_gnome:
                        if event.key == yellow_gnome.move_key[0] and yellow_gnome.jumping is False:
                            yellow_gnome.jumping = True
                            pygame.mixer.Sound.play(
                                pygame.mixer.Sound(f'data/sound/Jump{random.randint(1, 4)}.wav'))
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
        if not paused:
            for gnome in gnomes:
                gnome.move(gnomes)
                gnome.on_land()
                if gnome.dead:
                    gnomes.remove(gnome)
                    player_group.remove(gnome)
                for other in gnomes:
                    if pygame.sprite.collide_rect(gnome, other) and gnome != other:
                        gnome.rect.y -= 31
                        gnome.jumping = True
                        gnome.velocity_index = 10
                        break
        tiles_group.draw(screen)
        player_group.draw(screen)
        if paused:
            screen.blit(dim_screen, (0, 0))
            button('Continue', 330, 100, 120, 50, (245, 245, 220), (145, 145, 120), unpause)
            button('Restart', 330, 200, 120, 50, (245, 245, 220), (145, 145, 120), restart)
            button('Quit to menu', 330, 300, 120, 50, (245, 245, 220), (145, 145, 120), to_menu)
            button('Quit the game', 330, 400, 120, 50, (245, 245, 220), (145, 145, 120), terminate)
            button('Secret', 780, 480, 20, 20, (245, 245, 220), (145, 145, 120), secret)
        pygame.display.flip()
        clock.tick(FPS)


start_screen(screen)
