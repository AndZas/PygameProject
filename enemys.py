import pygame.draw

from particles import *

koeff = 10
createKD = 1.7 * 480
time = createKD
enemys = []
killedEnemys = 0


class Rect:
    def __init__(self, ParentScreen):
        self.parent = ParentScreen
        self.hp = 4
        self.speed = 0.25
        self.damage = 1
        self.color = pygame.Color('green')
        self.size = 40
        self.xp = {1: 2, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 150:
            player.playerGetDamage(self.pos, self.parent, killedEnemys)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y,
                          self.size, self.size), 4)


class Circle:
    def __init__(self, parentScreen):
        self.parent = parentScreen
        self.hp = 2
        self.speed = 1
        self.damage = 1
        self.size = 20
        self.xp = {1: 3, 2: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Circle.png'), (self.size, self.size))

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 25:
            player.playerGetDamage(self.pos, self.parent, killedEnemys)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        screen.blit(self.image,
                    (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y))


class Triangle:
    def __init__(self, parentScreen):
        self.parent = parentScreen
        self.hp = 3
        self.speed = 0.5
        self.damage = 1
        self.size = 40
        self.xp = {1: 3}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
        self.angle = 0
        self.image = pygame.transform.scale(pygame.image.load('images/Textures/Triangle.png'), (self.size, self.size))

    def update(self, player):
        self.angle += 0.1
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 70:
            player.playerGetDamage(self.pos, self.parent, killedEnemys)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.angle),
                    (self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y))


class Octagon:
    def __init__(self, parentScreen):
        self.parent = parentScreen
        self.hp = 15
        self.speed = 0.125
        self.damage = 1
        self.color = pygame.Color('darkgrey')
        self.size = 50
        self.xp = {1: 3, 2: 2, 3: 1}
        self.pos = self.x, self.y = (random.randint(0, self.parent.monResolution[0]),
                                     random.randint(0, self.parent.monResolution[1]))
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 400:
            player.playerGetDamage(self.pos, self.parent, killedEnemys)
        elif a > 1000:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
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


def updateEnemys(screen):
    global time, createKD, koeff, killedEnemys
    if time >= createKD:
        time = 0
        enemys.append(random.choice([Rect(screen), Triangle(screen), Circle(screen), Octagon(screen)]))
    else:
        time += 1.7
    for enemy in enemys:
        enemy.update(screen.player)
        for bullet in screen.player.bullets.bullets:
            if enemy.rect.collidepoint(*bullet.pos):
                screen.player.bullets.bullets.remove(bullet)
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    killedEnemys += 1
                    createParticlesXP(enemy.rect, enemy.xp, enemy.parent)
                    enemys.remove(enemy)
                    koeff -= 1


def drawEnemys(screen):
    for enemy in enemys:
        enemy.draw(screen)


def clearEnemies():
    global time, enemys, killedEnemys
    time = createKD
    enemys = []
    killedEnemys = 0
