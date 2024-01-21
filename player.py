from bullets import *
from hud import *
from ui import *


# Игрок
class Player:
    def __init__(self, parent):
        # Инициализация настроек игрока
        self.parent = parent
        self.pos = self.x, self.y = (self.parent.x + self.parent.size[0] // 2, self.parent.y + self.parent.size[1] // 2)
        self.size = 40
        self.speed = 0.75
        self.health = 10
        self.damage = 1
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
        self.coins = Coins()

    def draw(self):
        # Отрисовка персонажа на экране в зависимости от его размеров
        self.parent.screen.blit(self.image, (
            int(self.pos[0] - self.size // 2 - self.parent.x), int(self.pos[1] - self.size // 2 - self.parent.y)))

    def move(self, buttons):
        # Перемещение игрока
        self.getDamageKd += 1
        if self.getDamageKd > 240:
            self.image = self.afkImage

        self.time += 1
        if pygame.K_a in buttons and pygame.K_w in buttons:
            if self.pos[0] - self.parent.x - self.size // 2 > 0:
                self.x -= self.speed / 1.5
            if self.pos[1] - self.parent.y - self.size // 2 > 0:
                self.y -= self.speed / 1.5
        elif pygame.K_d in buttons and pygame.K_w in buttons:
            if self.pos[0] - self.parent.x + self.size // 2 < self.parent.size[0]:
                self.x += self.speed / 1.5
            if self.pos[1] - self.parent.y - self.size // 2 > 0:
                self.y -= self.speed / 1.5
        elif pygame.K_a in buttons and pygame.K_s in buttons:
            if self.pos[0] - self.parent.x - self.size // 2 > 0:
                self.x -= self.speed / 1.5
            if self.pos[1] - self.parent.y + self.size // 2 < self.parent.size[1]:
                self.y += self.speed / 1.5
        elif pygame.K_d in buttons and pygame.K_s in buttons:
            if self.pos[0] - self.parent.x + self.size // 2 < self.parent.size[0]:
                self.x += self.speed / 1.5
            if self.pos[1] - self.parent.y + self.size // 2 < self.parent.size[1]:
                self.y += self.speed / 1.5
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

    def playerGetDamage(self, enemyPos, screen, killedEnemys, damage1):
        # Получение урона игроком
        if self.getDamageKd >= 240:

            sound = r'sounds\Damage.wav'
            damage = pygame.mixer.Sound(sound).play(0, -1, False)
            if damage is not None:
                damage.set_volume(read_settings()[0])

            self.image = self.getDamageImage
            startPos = self.pos
            self.health -= damage1
            self.getDamageKd = 0
            vector = self.x - enemyPos[0], self.y - enemyPos[1]
            self.x += round(vector[0] * 2, 2)
            self.y += round(vector[1] * 2, 2)
            self.pos = self.x, self.y
            createParticlesDamage(startPos, self.pos, self.parent)
            if self.health <= 0:
                startEndWindow(self.xp, screen.timer.time * 10, self.bullets.shootedBullets, killedEnemys, self.parent.parent)

    def update(self):
        # Обновление позиций игрока
        if self.pos[0] - self.size // 2 <= self.parent.x:
            self.x += 1
        if self.pos[0] + self.size // 2 >= self.parent.x + self.parent.size[0]:
            self.x -= 1
        if self.pos[1] - self.size // 2 <= self.parent.y:
            self.y += 1
        if self.pos[1] + self.size // 2 >= self.parent.y + self.parent.size[1]:
            self.y -= 1
        self.pos = self.x, self.y

    def clear(self):
        # Очистка координат игрока
        self.pos = self.x, self.y = (self.parent.x + self.parent.size[0] // 2, self.parent.y + self.parent.size[1] // 2)
        self.health = 10
        self.xp = 0

        self.image = self.afkImage
        self.time = 0  # Количество кадров
