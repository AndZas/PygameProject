from bullets import *
from hud import *
from ui import *


class Player:
    def __init__(self, parent):
        # Инициализация настроек игрока
        self.parent = parent
        self.pos = self.x, self.y = (self.parent.x + self.parent.size[0] // 2, self.parent.y + self.parent.size[1] // 2)
        self.size = 40
        self.speed = 0.75
        self.health = 10
        self.maxHealth = 10
        self.xp = 0
        self.wallBunching = 30

        # Изображения
        self.afkImage = pygame.image.load('images/Textures/Player.png')
        self.getDamageImage = pygame.image.load('images/Textures/Player_GetDamage.png')
        self.image = self.afkImage

        self.kd = 120  # Количество кадров
        self.getDamageKd = 240  # Количество кадров
        self.time = 0  # Количество кадров

        self.bullets = Bullets(self)
        self.border = RedBorder()
        self.coins = Coins()

    def draw(self):
        # Отрисовка персонажа на экране в зависимости от его размеров
        self.parent.screen.blit(self.image, (
            self.pos[0] - self.size // 2 - self.parent.x, self.pos[1] - self.size // 2 - self.parent.y))

    def move(self, buttons):
        self.getDamageKd += 1
        if self.getDamageKd > 240:
            self.image = self.afkImage
            self.border.timer += 1

        # Перемещение игрока
        self.time += 1
        if pygame.K_a in buttons and pygame.K_w in buttons:
            if self.pos[0] - self.parent.x - self.size // 2 > 0:
                self.x -= math.sqrt(self.speed)
            if self.pos[1] - self.parent.y - self.size // 2 > 0:
                self.y -= math.sqrt(self.speed)
        elif pygame.K_d in buttons and pygame.K_w in buttons:
            if self.pos[0] - self.parent.x + self.size // 2 < self.parent.size[0]:
                self.x += math.sqrt(self.speed)
            if self.pos[1] - self.parent.y - self.size // 2 > 0:
                self.y -= math.sqrt(self.speed)
        elif pygame.K_a in buttons and pygame.K_s in buttons:
            if self.pos[0] - self.parent.x - self.size // 2 > 0:
                self.x -= math.sqrt(self.speed)
            if self.pos[1] - self.parent.y + self.size // 2 < self.parent.size[1]:
                self.y += math.sqrt(self.speed)
        elif pygame.K_d in buttons and pygame.K_s in buttons:
            if self.pos[0] - self.parent.x + self.size // 2 < self.parent.size[0]:
                self.x += math.sqrt(self.speed)
            if self.pos[1] - self.parent.y + self.size // 2 < self.parent.size[1]:
                self.y += math.sqrt(self.speed)
        elif pygame.K_a in buttons:
            if self.pos[0] - self.parent.x - self.size // 2 > 0:
                self.x -= self.speed
        elif pygame.K_d in buttons:
            if self.pos[0] - self.parent.x + self.size // 2 < self.parent.size[0]:
                self.x += self.speed
        elif pygame.K_w in buttons:
            if self.pos[1] - self.parent.y - self.size // 2 > 0:
                self.y -= self.speed
        elif pygame.K_s in buttons:
            if self.pos[1] - self.parent.y + self.size // 2 < self.parent.size[1]:
                self.y += self.speed
        self.pos = self.x, self.y

    def playerGetDamage(self, enemyPos, screen):
        if self.getDamageKd >= 240:
            self.image = self.getDamageImage
            startPos = self.pos
            self.health -= 1
            self.getDamageKd = 0
            vector = self.x - enemyPos[0], self.y - enemyPos[1]
            self.x += round(vector[0] * 2, 2)
            self.y += round(vector[1] * 2, 2)
            self.pos = self.x, self.y
            createParticlesDamage(startPos, self.pos, self.parent)
            if self.health <= 0:
                main2(self.xp, screen.timer.time)

    def update(self):
        if self.pos[0] - self.size // 2 <= self.parent.x:
            self.x += 1
        if self.pos[0] + self.size // 2 >= self.parent.x + self.parent.size[0]:
            self.x -= 1
        if self.pos[1] - self.size // 2 <= self.parent.y:
            self.y += 1
        if self.pos[1] + self.size // 2 >= self.parent.y + self.parent.size[1]:
            self.y -= 1
        self.pos = self.x, self.y
