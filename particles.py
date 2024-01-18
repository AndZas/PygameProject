import math
import random

import pygame

particles = []


class Particle:
    def __init__(self, pos, size):
        self.pos = self.x, self.y = pos
        self.size = size
        self.speed = 4
        self.playerDistance = 25
        self.color = pygame.Color('purple')
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size * 2)

    def update(self, player):
        vector = player.pos[0] - self.pos[0], player.pos[1] - self.pos[1]
        vecLen = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vecLen // self.speed
        if a <= 1:
            player.xp += self.size
            particles.remove(self)
        elif a <= self.playerDistance:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size * 2)


def createParticlesXP(rect, count):
    for size in count:
        for c in range(count[size]):
            coords = (random.randint(rect[0], rect[0] + rect[2]), random.randint(rect[1], rect[1] + rect[3]))
            particles.append(Particle(coords, size))


def updateParticlesXP(player):
    for part in particles:
        part.update(player)


def drawParticlesXP(screen):
    for part in particles:
        part.draw(screen)
