import pygame.draw

from particles import *

koeff = 10
createKD = 1.7 * 480
time = createKD
enemys = []


class Rect:
    def __init__(self):
        self.hp = 4
        self.speed = 1
        self.damage = 1
        self.color = pygame.Color('green')
        self.size = 40
        self.xp = {1: 2, 2: 1}
        self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        while 1000 > self.pos[0] > 0 and 1000 > self.pos[1] > 0:
            self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 25:
            player.playerGetDamage(self.pos)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size), 4)


class Circle:
    def __init__(self):
        self.hp = 2
        self.speed = 3
        self.damage = 1
        self.color = pygame.Color('blue')
        self.size = 20
        self.xp = {1: 3, 2: 1}
        self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        while 1000 > self.pos[0] > 0 and 1000 > self.pos[1] > 0:
            self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 8:
            player.playerGetDamage(self.pos)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size // 2, 4)


class Triangle:
    def __init__(self):
        self.hp = 3
        self.speed = 2
        self.damage = 1
        self.color = pygame.Color('yellow')
        self.size = 30
        self.xp = {1: 3}
        self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        while 1000 > self.pos[0] > 0 and 1000 > self.pos[1] > 0:
            self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        self.surf = pygame.Surface((self.size, self.size))
        self.angle = 0

    def update(self, player):
        self.angle += 1
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 15:
            player.playerGetDamage(self.pos)
        else:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect((*self.pos, self.size, self.size))

    def draw(self, screen):
        pygame.draw.lines(self.surf, self.color, False, [(self.size - self.size // 2, self.size // 2),
                                                      (self.size, self.size - self.size // 2),
                                                      (self.size // 2, self.size // 2),
                                                      (self.size - self.size // 2, self.y + self.size // 2)], 4)
        screen.blit(self.surf, self.pos)


class Octagon:
    def __init__(self):
        self.hp = 15
        self.speed = 0.5
        self.damage = 1
        self.color = pygame.Color('darkgrey')
        self.size = 50
        self.xp = {1: 3, 2: 2, 3: 1}
        self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        while 1000 > self.pos[0] > 0 and 1000 > self.pos[1] > 0:
            self.pos = self.x, self.y = random.randint(-500, 1500), random.randint(-500, 1500)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 15:
            player.playerGetDamage(self.pos)
        elif a > 250:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, [(self.x - self.size // 2, self.y + self.size // 4),
                                                      (self.x - self.size // 2, self.y - self.size // 4),
                                                      (self.x - self.size // 4, self.y - self.size // 2),
                                                      (self.x + self.size // 4, self.y - self.size // 2),
                                                      (self.x + self.size // 2, self.y - self.size // 4),
                                                      (self.x + self.size // 2, self.y + self.size // 4),
                                                      (self.x + self.size // 4, self.y + self.size // 2),
                                                      (self.x - self.size // 4, self.y + self.size // 2),
                                                      (self.x - self.size // 2, self.y + self.size // 4)], 4)


def updateEnemys(player):
    global time, createKD, koeff
    if time >= createKD:
        time = 0
        enemys.append(random.choice([Rect(), Circle(), Triangle(), Octagon()][:]))
    else:
        time += 1.7
    for enemy in enemys:
        enemy.update(player)
        for bullet in player.bullets.bullets:
            if enemy.rect.collidepoint(*bullet.pos):
                player.bullets.bullets.remove(bullet)
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    createParticlesXP(enemy.rect, enemy.xp)
                    enemys.remove(enemy)
                    koeff -= 1


def drawEnemys(screen):
    for enemy in enemys:
        enemy.draw(screen)
