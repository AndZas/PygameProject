import math

import pygame


# Класс одной пули
class Bullet:
    def __init__(self, PlayerPos, MousePos):
        self.speed = 5
        self.damage = 1
        self.pos = PlayerPos
        self.size = 2
        self.color = pygame.Color('white')

        # Расчет вектора движения пули каждый кадр
        vect = (MousePos[0] - PlayerPos[0], MousePos[1] - PlayerPos[1])
        vectLen = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        self.resVect = (round(vect[0] / (vectLen / self.speed), 2), round(vect[1] / (vectLen / self.speed), 2))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.size // 2, self.pos[1] - self.size // 2), 2)

    def update(self):
        self.pos = (self.pos[0] + self.resVect[0], self.pos[1] + self.resVect[1])


# Класс обновления всего массива пуль
class Bullets:
    def __init__(self, parent):
        self.parent = parent
        self.bullets = []

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos[0] <= 0 or bullet.pos[0] >= self.parent.parent.size[0] or bullet.pos[1] <= 0 or bullet.pos[
                1] >= self.parent.parent.size[1]:
                self.parent.parent.resizeWindowPlus(bullet.pos)
                self.bullets.remove(bullet)

    def shoot(self, pos):
        self.bullets.append(
            Bullet((self.parent.pos[0], self.parent.pos[1]), pos))

    def draw(self):
        for bullet in self.bullets:
            bullet.draw(self.parent.parent.screen)
