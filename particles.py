import math
import random

import pygame

from read_files import read_settings, read_money_and_health, dump_money_and_health

particlesXP = []
particles = []


# Частицы опыта
class ParticleXp:
    def __init__(self, pos, size, parentScreen):
        self.parent = parentScreen
        self.pos = self.x, self.y = pos
        self.size = size
        self.speed = 4
        self.playerDistance = 25
        self.color = pygame.Color('purple')
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.parent.x, self.pos[1] - self.parent.y),
                           self.size * 2)

    # Обновление
    def update(self, player):
        temp = read_money_and_health()
        player.xp = temp[0]
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 1:
            sound = random.choice([r'sounds\Get_Xp1.wav', r'sounds\Get_Xp2.wav'])
            xp = pygame.mixer.Sound(sound).play(0, -1, False)
            if xp is not None:
                xp.set_volume(read_settings()[0])

            player.xp += self.size
            dump_money_and_health(player.xp, temp[1])
            player.xp_for_end += self.size
            player.coins.count += self.size
            particlesXP.remove(self)
        elif a <= self.playerDistance:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size * 2)


# Создание частиц опыта
def createParticlesXP(rect, count, ParentScreen):
    for size in count:
        for c in range(count[size]):
            coords = (random.randint(rect[0], rect[0] + rect[2]), random.randint(rect[1], rect[1] + rect[3]))
            particlesXP.append(ParticleXp(coords, size, ParentScreen))


# Частицы от выстрелов
class ParticleShoot:
    def __init__(self, startPos, endPos, screen, orientation):
        self.orientation = orientation
        self.screen = screen
        self.startPos = startPos
        self.endPos = endPos
        self.pos = self.startPos
        self.speed = random.uniform(0.5, 2)
        self.size = random.randint(1, 3)
        color = random.randint(100, 200)
        self.color = (color, color, color)

        # Расчет вектора
        vect = (endPos[0] - startPos[0], endPos[1] - startPos[1])
        vectLen = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        a = vectLen / self.speed
        self.resVect = (round(vect[0] / a, 5), round(vect[1] / a, 5))

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

    # Обновление
    def update(self):
        self.pos = (self.pos[0] + self.resVect[0], self.pos[1] + self.resVect[1])
        if ((int(self.pos[0]) >= self.endPos[0] and (
                int(self.pos[1]) >= self.endPos[1] or int(self.pos[1]) <= self.endPos[
            1])) and self.orientation == 'left') or ((int(self.pos[0]) <= self.endPos[0] and (
                int(self.pos[1]) >= self.endPos[1] or int(self.pos[1]) <= self.endPos[
            1])) and self.orientation == 'right') or (
                (int(self.pos[0]) >= self.endPos[0] or int(self.pos[0]) <= self.endPos[0]) and int(self.pos[1]) <=
                self.endPos[1] and self.orientation == 'down') or (
                (int(self.pos[0]) >= self.endPos[0] or int(self.pos[0]) <= self.endPos[0]) and int(self.pos[1]) >=
                self.endPos[1] and self.orientation == 'up'):
            particles.remove(self)


# Создание частиц от выстрелов
def createParticlesShoot(pos, orientation, ParentScreen):
    for i in range(random.randint(3, 8)):
        if orientation == 'left':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]), int(pos[0]) + 80), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              ParentScreen, orientation))
        if orientation == 'right':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 80, int(pos[0])), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              ParentScreen, orientation))
        if orientation == 'down':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]) - 80, int(pos[1]))),
                              ParentScreen, orientation))
        if orientation == 'up':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]), int(pos[1]) + 80)),
                              ParentScreen, orientation))


# Частицы получения урона
class ParticleDamage:
    def __init__(self, startPos, endPos, screen):
        self.way = 0
        self.screen = screen
        self.startPos = startPos
        self.endPos = endPos
        self.pos = self.startPos
        self.speed = random.uniform(0.5, 1)
        self.size = random.randint(1, 3)
        self.color = (random.randint(100, 200), random.randint(0, 20), random.randint(0, 20))

        # Расчет вектора
        vect = (endPos[0] - startPos[0], endPos[1] - startPos[1])
        vectLen = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        a = vectLen / self.speed
        self.resVect = (round(vect[0] / a, 5), round(vect[1] / a, 5))

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

    # Обновление
    def update(self):
        self.way += 1
        self.pos = (self.pos[0] + self.resVect[0], self.pos[1] + self.resVect[1])
        if self.way >= 120:
            particles.remove(self)


# Создание частиц урона
def createParticlesDamage(startPos, endPos, ParentScreen):
    for i in range(random.randint(3, 8)):
        if startPos[0] > endPos[0] and startPos[1] + 60 > endPos[1] > startPos[1] - 60:
            particles.append(
                ParticleDamage(startPos, (int(endPos[0]), random.randint(int(endPos[1] - 20), int(endPos[1] + 20))),
                               ParentScreen))
        if startPos[0] < endPos[0] and startPos[1] + 60 > endPos[1] > startPos[1] - 60:
            particles.append(
                ParticleDamage(startPos, (int(endPos[0]), random.randint(int(endPos[1] - 20), int(endPos[1] + 20))),
                               ParentScreen))
        if startPos[1] > endPos[1] and startPos[0] + 60 > endPos[0] > startPos[0] - 60:
            particles.append(
                ParticleDamage(startPos, (random.randint(int(endPos[0] - 60), int(endPos[0] + 60)), endPos[1]),
                               ParentScreen))
        if startPos[1] < endPos[1] and startPos[0] + 60 > endPos[0] > startPos[0] - 60:
            particles.append(
                ParticleDamage(startPos, (random.randint(int(endPos[0] - 60), int(endPos[0] + 60)), endPos[1]),
                               ParentScreen))


# Частицы смерти врагов
class ParticleKilled:
    def __init__(self, startPos, endPos, color, screen):
        self.way = 0
        self.screen = screen
        self.startPos = startPos
        self.endPos = endPos
        self.pos = self.startPos
        self.speed = random.uniform(0.5, 1)
        self.size = random.randint(1, 3)
        self.color = color

        # Расчет вектора
        vect = (endPos[0] - startPos[0], endPos[1] - startPos[1])
        vectLen = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        a = vectLen / self.speed
        self.resVect = (round(vect[0] / a, 5), round(vect[1] / a, 5))

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

    # Обновление
    def update(self):
        self.way += 1
        self.pos = (self.pos[0] + self.resVect[0], self.pos[1] + self.resVect[1])
        if self.way >= 120:
            particles.remove(self)


# Создание частиц смерти врагов
def createParticlesKilled(startPos, ParentScreen, color, size):
    for i in range(random.randint(3, 8)):
        endPos = (random.randint(int(startPos[0]) - size // 2, int(startPos[0]) + size // 2),
                  random.randint(int(startPos[1]) - size // 2, int(startPos[1]) + size // 2))
        particles.append(ParticleKilled(startPos, (int(endPos[0]), int(endPos[1])), color, ParentScreen))


# Отрисовка частиц
def drawParticles(screen):
    for particle in particles:
        particle.draw(screen)
    for particle in particlesXP:
        particle.draw(screen)


# Обновление частиц
def updateParticles():
    for particle in particles:
        particle.update()


# Обновление частиц опыта
def updateParticlesXP(screen):
    for particle in particlesXP:
        particle.update(screen)


# Очистка частиц
def clearParticles():
    global particles
    particles = []
    particlesXP = []
