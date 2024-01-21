import sys
from time import sleep
import pygame.draw
from particles import *
import sqlite3
from widgets import Text
from read_files import read_settings, dump_settings

koeff = 10
createKD = 1.7 * 480
time = createKD
enemys = []
killedEnemys = 0
killedEnemys_for_end = 0


def update_level():
    global enemies, speed_koeff, speed_koeff, damage_koeff, health_koeff, to_next_lvl, lvl
    lvl = read_settings()[-1]
    con = sqlite3.connect("Levels")
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Levels WHERE Number = '{lvl}'").fetchall()
    con.close()
    enemies = result[0][1].split(', ')
    speed_koeff = result[0][2]
    damage_koeff = result[0][3]
    health_koeff = result[0][4]
    to_next_lvl = result[0][5]


update_level()


# Прямоугольник
class Rect:
    def __init__(self, ParentScreen, hp=4, speed=0.25, damage=1):
        self.parent = ParentScreen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.color = pygame.Color('green')
        self.size = 40
        self.xp = {1: 2, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] and self.parent.y < self.pos[
            1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                         random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 150:
            player.playerGetDamage(self.pos, self.parent, killedEnemys_for_end, self.damage)
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
    def __init__(self, parentScreen, hp=2, speed=1, damage=1):
        self.parent = parentScreen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.size = 20
        self.xp = {1: 3, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] and self.parent.y < self.pos[
            1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                         random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Circle.png'), (self.size, self.size))
        self.color = pygame.Color('aqua')

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 25:
            player.playerGetDamage(self.pos, self.parent, killedEnemys_for_end, self.damage)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        screen.blit(self.image,
                    (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y))

    def __str__(self):
        return 'Circle'


# Треугольник
class Triangle:
    def __init__(self, parentScreen, hp=3, speed=0.5, damage=1):
        self.parent = parentScreen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.size = 40
        self.xp = {1: 3}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] and self.parent.y < self.pos[
            1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                         random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.angle = 0
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Triangle.png'), (self.size, self.size))
        self.color = pygame.Color('yellow')

    def update(self, player):
        # Обновление врага
        self.angle += 0.1
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 70:
            player.playerGetDamage(self.pos, self.parent, killedEnemys_for_end, self.damage)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        # Отрисовка врага
        screen.blit(pygame.transform.rotate(self.image, self.angle),
                    (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y))

    def __str__(self):
        return 'Triangle'


# Восьмиугольник
class Octagon:
    def __init__(self, parentScreen, hp=15, speed=0.125, damage=1):
        self.parent = parentScreen
        self.hp = hp * health_koeff
        self.speed = speed * speed_koeff
        self.damage = damage * damage_koeff
        self.color = pygame.Color('darkgrey')
        self.size = 50
        self.xp = {1: 3, 2: 2, 3: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        while self.parent.x < self.pos[0] < self.parent.x + self.parent.size[0] and self.parent.y < self.pos[
            1] < self.parent.y + self.parent.size[1]:
            self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                         random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        # Обновление врага
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 400:
            player.playerGetDamage(self.pos, self.parent, killedEnemys_for_end, self.damage)
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


# Обновление всех врагов
def updateEnemys(screen):
    global time, createKD, koeff, killedEnemys_for_end, killedEnemys
    lst = [Rect(screen), Triangle(screen), Circle(screen), Octagon(screen)]
    choice = []
    for i in range(len(lst)):
        if str(lst[i]) in enemies:
            choice.append(lst[i])
    if time >= createKD:
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
                    killedEnemys_for_end += 1
                    killedEnemys += 1
                    createParticlesKilled(enemy.pos, screen, enemy.color, enemy.size)
                    createParticlesXP(enemy.rect, enemy.xp, enemy.parent)
                    enemys.remove(enemy)
                    koeff -= 1

    if killedEnemys == to_next_lvl:
        dump_settings(1)
        killedEnemys = 0
        r = True
        while r:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    r = False
            Text((0, screen.screen.get_height() // 2), 40, f'Level: {lvl + 1}', center_x=True,
                 color=pygame.Color('white')).render(screen.screen)
            pygame.display.update()
        update_level()
        screen.parent.buttonsPressed = []


# Отрисовка всех врагов
def drawEnemys(screen):
    for enemy in enemys:
        enemy.draw(screen)


# Очистка врагов при перезапуске
def clearEnemies():
    global time, enemys, killedEnemys_for_end, killedEnemys
    time = createKD
    enemys = []
    killedEnemys_for_end = 0
    killedEnemys = 0
