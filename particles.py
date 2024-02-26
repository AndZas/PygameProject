import math
import random
import pygame
from read_files import read_settings, read_money_and_health, dump_money_and_health

particles_xp = []
particles = []


# Общий инит для ParticleDamage и ParticleKilled
class Init:
    def __init__(self, start_pos, end_pos, screen):
        self.screen = screen
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pos = self.start_pos
        self.speed = random.uniform(0.5, 1)
        self.size = random.randint(1, 3)
        self.way = 0
        # Расчет вектора
        vect = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        vect_len = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        a = vect_len / self.speed
        self.res_vect = (round(vect[0] / a, 5), round(vect[1] / a, 5))

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

    # Обновление
    def update(self):
        self.way += 1
        self.pos = (self.pos[0] + self.res_vect[0], self.pos[1] + self.res_vect[1])
        if self.way >= 120:
            particles.remove(self)


# Частицы опыта
class ParticleXp:
    def __init__(self, pos, size, parent_screen):
        self.parent = parent_screen
        self.pos = self.x, self.y = pos
        self.size = size
        self.speed = 4
        self.player_distance = 25
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
        vec_len = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        a = vec_len // self.speed
        if a <= 1:
            sound = random.choice([r'sounds\Get_Xp1.wav', r'sounds\Get_Xp2.wav'])
            xp = pygame.mixer.Sound(sound).play(0, -1, False)
            if xp is not None:
                xp.set_volume(read_settings()[0])

            player.xp += self.size
            dump_money_and_health(player.xp, temp[1])
            player.xp_for_end += self.size
            player.coins.count += self.size
            particles_xp.remove(self)
        elif a <= self.player_distance:
            self.x += round(vector[0] / a, 3)
            self.y += round(vector[1] / a, 3)
        self.pos = (self.x, self.y)
        self.rect = pygame.Rect(self.pos[0] - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size * 2)


# Создание частиц опыта
def create_particles_xp(rect, count, parent_screen):
    for size in count:
        for c in range(count[size]):
            coords = (random.randint(rect[0], rect[0] + rect[2]), random.randint(rect[1], rect[1] + rect[3]))
            particles_xp.append(ParticleXp(coords, size, parent_screen))


# Частицы от выстрелов
class ParticleShoot:
    def __init__(self, start_pos1, end_pos1, screen, orientation):
        self.orientation = orientation
        self.screen = screen
        self.start_pos = start_pos1
        self.end_pos = end_pos1
        self.pos = self.start_pos
        self.speed = random.uniform(0.5, 2)
        self.size = random.randint(1, 3)
        color = random.randint(100, 200)
        self.color = (color, color, color)

        # Расчет вектора
        vect = (end_pos1[0] - start_pos1[0], end_pos1[1] - start_pos1[1])
        vect_len = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        a = vect_len / self.speed
        self.res_vect = (round(vect[0] / a, 5), round(vect[1] / a, 5))

    # Отрисовка
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0] - self.screen.x, self.pos[1] - self.screen.y), self.size)

    # Обновление
    def update(self):
        self.pos = (self.pos[0] + self.res_vect[0], self.pos[1] + self.res_vect[1])
        if ((int(self.pos[0]) >= self.end_pos[0] and
             (int(self.pos[1]) >= self.end_pos[1] or
              int(self.pos[1]) <= self.end_pos[1])) and self.orientation == 'left') \
                or ((int(self.pos[0]) <= self.end_pos[0] and (int(self.pos[1]) >= self.end_pos[1]
                                                              or int(self.pos[1]) <= self.end_pos[1]))
                    and self.orientation == 'right') or ((int(self.pos[0]) >= self.end_pos[0]
                                                          or int(self.pos[0]) <= self.end_pos[0])
                                                         and int(self.pos[1]) <= self.end_pos[1]
                                                         and self.orientation == 'down') \
                or ((int(self.pos[0]) >= self.end_pos[0] or int(self.pos[0]) <= self.end_pos[0])
                    and int(self.pos[1]) >= self.end_pos[1] and self.orientation == 'up'):
            particles.remove(self)


# Создание частиц от выстрелов
def create_particles_shoot(pos, orientation, parent_screen):
    for i in range(random.randint(3, 8)):
        if orientation == 'left':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]), int(pos[0]) + 80), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              parent_screen, orientation))
        if orientation == 'right':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 80, int(pos[0])), random.randint(int(pos[1]) - 40, int(pos[1]) + 40)),
                              parent_screen, orientation))
        if orientation == 'down':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]) - 80, int(pos[1]))),
                              parent_screen, orientation))
        if orientation == 'up':
            particles.append(
                ParticleShoot(pos, (
                    random.randint(int(pos[0]) - 40, int(pos[0]) + 40), random.randint(int(pos[1]), int(pos[1]) + 80)),
                              parent_screen, orientation))


# Частицы получения урона
class ParticleDamage(Init):
    def __init__(self, start_pos, end_pos, screen):
        Init.__init__(self, start_pos, end_pos, screen)
        self.color = (random.randint(100, 200), random.randint(0, 20), random.randint(0, 20))


# Создание частиц урона
def create_particles_damage(start_pos, end_pos, parent_screen):
    for i in range(random.randint(3, 8)):
        if start_pos[0] > end_pos[0] and start_pos[1] + 60 > end_pos[1] > start_pos[1] - 60:
            particles.append(
                ParticleDamage(start_pos, (int(end_pos[0]), random.randint(int(end_pos[1] - 20), int(end_pos[1] + 20))),
                               parent_screen))
        if start_pos[0] < end_pos[0] and start_pos[1] + 60 > end_pos[1] > start_pos[1] - 60:
            particles.append(
                ParticleDamage(start_pos, (int(end_pos[0]), random.randint(int(end_pos[1] - 20), int(end_pos[1] + 20))),
                               parent_screen))
        if start_pos[1] > end_pos[1] and start_pos[0] + 60 > end_pos[0] > start_pos[0] - 60:
            particles.append(
                ParticleDamage(start_pos, (random.randint(int(end_pos[0] - 60), int(end_pos[0] + 60)), end_pos[1]),
                               parent_screen))
        if start_pos[1] < end_pos[1] and start_pos[0] + 60 > end_pos[0] > start_pos[0] - 60:
            particles.append(
                ParticleDamage(
                    start_pos, (random.randint(int(end_pos[0] - 60), int(end_pos[0] + 60)), end_pos[1]), parent_screen
                )
            )


# Частицы смерти врагов
class ParticleKilled(Init):
    def __init__(self, start_pos, end_pos, screen, color):
        Init.__init__(self, start_pos, end_pos, screen)
        self.color = color


# Создание частиц смерти врагов
def create_particles_killed(start_pos, parent_screen, color, size):
    for i in range(random.randint(3, 8)):
        end_pos = (random.randint(int(start_pos[0]) - size // 2, int(start_pos[0]) + size // 2),
                   random.randint(int(start_pos[1]) - size // 2, int(start_pos[1]) + size // 2))
        particles.append(ParticleKilled(start_pos, (int(end_pos[0]), int(end_pos[1])), parent_screen, color))


# Отрисовка частиц
def draw_particles(screen):
    for particle in particles:
        particle.draw(screen)
    for particle in particles_xp:
        particle.draw(screen)


# Обновление частиц
def update_particles():
    for particle in particles:
        particle.update()


# Обновление частиц опыта
def update_particles_xp(screen):
    for particle in particles_xp:
        particle.update(screen)


# Очистка частиц
def clear_particles():
    global particles
    particles = []
