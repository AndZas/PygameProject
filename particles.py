import math
import random

import pygame

particlesXP = []
particlesShoot = []


class ParticleXp:
    def __init__(self, pos, size, parentScreen):
        self.parent = parentScreen
        self.pos = self.x, self.y = pos
        self.size = size
        self.speed = 4
        self.playerDistance = 25
        self.color = pygame.Color('purple')
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.parent.x, self.pos[1] - self.parent.y), self.size * 2)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 1:
            player.xp += self.size
            particlesXP.remove(self)
        elif a <= self.playerDistance:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size * 2)


def createParticlesXP(rect, count, ParentScreen):
    for size in count:
        for c in range(count[size]):
            coords = (random.randint(rect[0], rect[0] + rect[2]), random.randint(rect[1], rect[1] + rect[3]))
            particlesXP.append(ParticleXp(coords, size, ParentScreen))


def updateParticlesXP(player):
    for part in particlesXP:
        part.update(player)


def drawParticlesXP(screen):
    for part in particlesXP:
        part.draw(screen)


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

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

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
            particlesShoot.remove(self)


def createParticlesShoot(pos, orientation, ParentScreen):
    for i in range(random.randint(3, 8)):
        if orientation == 'left':
            particlesShoot.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]), int(pos[0]) + 80), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              ParentScreen, orientation))
        if orientation == 'right':
            particlesShoot.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 80, int(pos[0])), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              ParentScreen, orientation))
        if orientation == 'down':
            particlesShoot.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]) - 80, int(pos[1]))),
                              ParentScreen, orientation))
        if orientation == 'up':
            particlesShoot.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]), int(pos[1]) + 80)),
                              ParentScreen, orientation))


def drawParticlesShoot(screen):
    for particle in particlesShoot:
        particle.draw(screen)


def updateParticlesShoot():
    for particle in particlesShoot:
        particle.update()
