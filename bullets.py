from particles import *


# Класс одной пули
class Bullet:
    def __init__(self, PlayerPos, MousePos, parent):
        self.parent = parent
        self.speed = 2.5
        self.damage = 1
        self.pos = PlayerPos
        self.size = 2
        self.color = pygame.Color('white')

        # Расчет вектора движения пули
        vect = (
            MousePos[0] - (PlayerPos[0] - self.parent.parent.x), MousePos[1] - (PlayerPos[1] - self.parent.parent.y))
        vectLen = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        self.resVect = (round(vect[0] / (vectLen / self.speed), 2), round(vect[1] / (vectLen / self.speed), 2))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (
            self.pos[0] - self.size // 2 - self.parent.parent.x, self.pos[1] - self.size // 2 - self.parent.parent.y),
                           2)

    def update(self):
        self.pos = (self.pos[0] + self.resVect[0], self.pos[1] + self.resVect[1])


# Класс обновления всего массива пуль
class Bullets:
    def __init__(self, parent):
        self.parent = parent
        self.bullets = []
        self.shootedBullets = 0

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos[0] - self.parent.parent.x <= 0 or bullet.pos[
                0] - self.parent.parent.x >= self.parent.parent.size[0] or bullet.pos[
                1] - self.parent.parent.y <= 0 or bullet.pos[
                1] - self.parent.parent.y >= self.parent.parent.size[1]:
                if bullet.pos[0] - self.parent.parent.x <= 0:
                    createParticlesShoot(bullet.pos, 'left', self.parent.parent)
                elif bullet.pos[0] - self.parent.parent.x >= self.parent.parent.size[0]:
                    createParticlesShoot(bullet.pos, 'right', self.parent.parent)
                elif bullet.pos[1] - self.parent.parent.y <= 0:
                    createParticlesShoot(bullet.pos, 'up', self.parent.parent)
                elif bullet.pos[1] - self.parent.parent.y >= self.parent.parent.size[1]:
                    createParticlesShoot(bullet.pos, 'down', self.parent.parent)
                self.parent.parent.resizeWindowPlus(bullet.pos)
                self.bullets.remove(bullet)

    def shoot(self, pos):
        self.shootedBullets += 1
        self.bullets.append(
            Bullet((self.parent.pos[0], self.parent.pos[1]),
                   pos, self.parent))

    def draw(self):
        for bullet in self.bullets:
            bullet.draw(self.parent.parent.screen)
