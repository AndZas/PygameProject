import pygame.draw
from particles import *
import sqlite3
from widgets import Text, NextLevelNotification
from read_files import read_lvl, dump_lvl

koeff = 10
create_kd = 1.7 * 480
time = create_kd
enemys = []
killed_enemys = 0
killed_enemys_for_end = 0
enemies = None
speed_koeff = None
damage_koeff = None
health_koeff = None
to_next_lvl = None
lvl = None


# Прямоугольник
class Rect:
    def __init__(self, parent_screen, hp=4, speed=0.25, damage=1):
        self.parent = parent_screen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.color = pygame.Color('green')
        self.size = 40
        self.xp = {1: 2, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                     random.randint(0, self.parent.mon_resolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] \
                and self.parent.y < self.pos[1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                         random.randint(0, self.parent.mon_resolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vec_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vec_len // self.speed
        if a <= 150:
            player.player_get_damage(self.pos, self.parent, killed_enemys_for_end, self.damage)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        pygame.draw.rect(screen, self.color,
                         (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y,
                          self.size, self.size), 4)

    def __str__(self):
        return 'Rect'


# Круг
class Circle:
    def __init__(self, parent_screen, hp=2, speed=1, damage=1):
        self.parent = parent_screen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.size = 20
        self.xp = {1: 3, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                     random.randint(0, self.parent.mon_resolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] \
                and self.parent.y < self.pos[1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                         random.randint(0, self.parent.mon_resolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Circle.png'), (self.size, self.size))
        self.color = pygame.Color('aqua')

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vec_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vec_len // self.speed
        if a <= 25:
            player.player_get_damage(self.pos, self.parent, killed_enemys_for_end, self.damage)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        screen.blit(
            self.image, (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y)
        )

    def __str__(self):
        return 'Circle'


# Треугольник
class Triangle:
    def __init__(self, parent_screen, hp=3, speed=0.5, damage=1):
        self.parent = parent_screen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.size = 40
        self.xp = {1: 3}
        self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                     random.randint(0, self.parent.mon_resolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] \
                and self.parent.y < self.pos[1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                         random.randint(0, self.parent.mon_resolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.angle = 0
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Triangle.png'), (self.size, self.size))
        self.color = pygame.Color('yellow')

    def update(self, player):
        # Обновление врага
        self.angle += 0.1
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vec_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vec_len // self.speed
        if a <= 70:
            player.player_get_damage(self.pos, self.parent, killed_enemys_for_end, self.damage)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        screen.blit(
            pygame.transform.rotate(self.image, self.angle),
            (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y)
        )

    def __str__(self):
        return 'Triangle'


# Восьмиугольник
class Octagon:
    def __init__(self, parent_screen, hp=15, speed=0.125, damage=1):
        self.parent = parent_screen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.color = pygame.Color('darkgrey')
        self.size = 50
        self.xp = {1: 3, 2: 2, 3: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                     random.randint(0, self.parent.mon_resolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] \
                and self.parent.y < self.pos[1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.mon_resolution[0]),
                                         random.randint(0, self.parent.mon_resolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vec_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vec_len // self.speed
        if a <= 400:
            player.player_get_damage(self.pos, self.parent, killed_enemys_for_end, self.damage)
        elif a > 1000:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        pygame.draw.lines(screen, self.color, False,
                          [(self.x - self.size // 2 - self.parent.x, self.y + self.size // 4 - self.parent.y),
                           (self.x - self.size // 2 - self.parent.x, self.y - self.size // 4 - self.parent.y),
                           (self.x - self.size // 4 - self.parent.x, self.y - self.size // 2 - self.parent.y),
                           (self.x + self.size // 4 - self.parent.x, self.y - self.size // 2 - self.parent.y),
                           (self.x + self.size // 2 - self.parent.x, self.y - self.size // 4 - self.parent.y),
                           (self.x + self.size // 2 - self.parent.x, self.y + self.size // 4 - self.parent.y),
                           (self.x + self.size // 4 - self.parent.x, self.y + self.size // 2 - self.parent.y),
                           (self.x - self.size // 4 - self.parent.x, self.y + self.size // 2 - self.parent.y),
                           (self.x - self.size // 2 - self.parent.x, self.y + self.size // 4 - self.parent.y)], 4)

    def __str__(self):
        return 'Octagon'


def update_level():
    global enemies, speed_koeff, damage_koeff, health_koeff, to_next_lvl, lvl
    lvl = read_lvl()
    con = sqlite3.connect("files_txt_json_db/Levels")
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Levels WHERE Number = '{lvl}'").fetchall()
    con.close()
    enemies = result[0][1].split(', ')
    speed_koeff = result[0][2]
    damage_koeff = result[0][3]
    health_koeff = result[0][4]
    to_next_lvl = result[0][5]


# Обновление всех врагов
def update_enemys(screen):
    update_level()
    global time, create_kd, koeff, killed_enemys_for_end, killed_enemys
    lst = [Rect(screen), Triangle(screen), Circle(screen), Octagon(screen)]
    choice = []
    for i in range(len(lst)):
        if str(lst[i]) in enemies:
            choice.append(lst[i])
    if time >= create_kd:
        time = 0
        enemys.append(random.choice(choice))
    else:
        time += 1.7
    for enemy in enemys:
        enemy.update(screen.player)
        for bullet in screen.player.bullets.bullets:
            if enemy.rect.collidepoint(*bullet.pos):
                screen.player.bullets.bullets.remove(bullet)
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    killed_enemys_for_end += 1
                    killed_enemys += 1
                    create_particles_killed(enemy.pos, screen, enemy.color, enemy.size)
                    create_particles_xp(enemy.rect, enemy.xp, enemy.parent)
                    enemys.remove(enemy)
                    koeff -= 1

    if killed_enemys == to_next_lvl:
        # После прохождения уровня открывается окно
        t1 = Text((0, 20), 20, 'Congratulations!',
                  center_x=Text, color=pygame.Color('purple'))
        t2 = Text((0, 50), 20, 'You have passed this level',
                  center_x=Text, color=pygame.Color('purple'))

        menu = NextLevelNotification((30, 240), 20, 'menu', color=pygame.Color('purple'))
        next_lvl = NextLevelNotification((180, 240), 20, 'next level', color=pygame.Color('purple'))
        running = True
        pygame.display.set_mode((300, 300))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.flag = False
                    running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if next_lvl.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    running = False
                    pygame.time.delay(300)
            elif menu.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    screen.flag = False
                    running = False
            next_lvl.render(screen.screen)
            menu.render(screen.screen)
            t1.render(screen.screen)
            t2.render(screen.screen)
            pygame.display.update()
        dump_lvl(lvl + 1)
        screen.clear_ = True
        update_level()


# Отрисовка всех врагов
def draw_enemys(screen):
    for enemy in enemys:
        enemy.draw(screen)


# Очистка врагов при перезапуске
def clear_enemies():
    global time, enemys, killed_enemys_for_end, killed_enemys
    time = create_kd
    enemys = []
    killed_enemys_for_end = 0
    killed_enemys = 0
