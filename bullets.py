from particles import *
from read_files import read_settings


# Класс одной пули
class Bullet:
    def __init__(self, player_pos, mouse_pos, parent):
        self.parent = parent
        self.speed = 2.5
        self.damage = self.parent.damage
        self.pos = player_pos
        self.size = 2
        self.color = pygame.Color('white')

        # Расчет вектора движения пули
        vect = (mouse_pos[0] - (player_pos[0] - self.parent.parent.x),
                mouse_pos[1] - (player_pos[1] - self.parent.parent.y))
        vect_len = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
        self.res_vect = (round(vect[0] / (vect_len / self.speed), 2), round(vect[1] / (vect_len / self.speed), 2))

    # Отрисовка пули
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (
            self.pos[0] - self.size // 2 - self.parent.parent.x, self.pos[1] - self.size // 2 - self.parent.parent.y),
                           2)

    # Обновление пули
    def update(self):
        self.pos = (self.pos[0] + self.res_vect[0], self.pos[1] + self.res_vect[1])


# Класс обновления всего массива пуль
class Bullets:
    def __init__(self, parent):
        self.parent = parent
        self.bullets = []
        self.shooted_bullets = 0

    # Обновление всего списка пуль
    def update(self):
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos[0] - self.parent.parent.x <= 0 \
                    or bullet.pos[0] - self.parent.parent.x >= self.parent.parent.size[0] \
                    or bullet.pos[1] - self.parent.parent.y <= 0 \
                    or bullet.pos[1] - self.parent.parent.y >= self.parent.parent.size[1]:
                if bullet.pos[0] - self.parent.parent.x <= 0:
                    create_particles_shoot(bullet.pos, 'left', self.parent.parent)
                elif bullet.pos[0] - self.parent.parent.x >= self.parent.parent.size[0]:
                    create_particles_shoot(bullet.pos, 'right', self.parent.parent)
                elif bullet.pos[1] - self.parent.parent.y <= 0:
                    create_particles_shoot(bullet.pos, 'up', self.parent.parent)
                elif bullet.pos[1] - self.parent.parent.y >= self.parent.parent.size[1]:
                    create_particles_shoot(bullet.pos, 'down', self.parent.parent)
                sound = r'sounds\assets_sounds_impact.wav'
                impact = pygame.mixer.Sound(sound).play(0, -1, False)
                if impact is not None:
                    impact.set_volume(read_settings()[0])

                self.parent.parent.resize_window_plus(bullet.pos, self.parent.wall_bunching)
                self.bullets.remove(bullet)

    # Выстрел при нажатии на ЛКМ
    def shoot(self, pos):
        sound = r'sounds\Shoot.wav'
        shoot = pygame.mixer.Sound(sound).play(0, -1, False)
        if shoot is not None:
            shoot.set_volume(read_settings()[0])

        self.shooted_bullets += 1
        self.bullets.append(
            Bullet((self.parent.pos[0], self.parent.pos[1]), pos, self.parent))

    # Отрисовка всего списка пуль
    def draw(self):
        for bullet in self.bullets:
            bullet.draw(self.parent.parent.screen)

    # Очистка позиций пуль
    def clear(self):
        self.bullets = []
        self.shooted_bullets = 0
