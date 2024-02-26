from pygame._sdl2.video import Window
from screeninfo import get_monitors
import os
from enemys import *
from player import *


# Экран
def get_monitor_resolution():
    # Возвращает разрешение монитора
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor.width, monitor.height


class Screen:
    def __init__(self, parent=None):
        # Настройки окна
        self.clear_ = False
        self.clear_points = False
        self.flag = True
        self.parent = parent
        self.min_size = (300, 300)
        self.size = self.width, self.height = (500, 500)
        self.mon_resolution = get_monitor_resolution()
        self.pos = self.x, self.y = (
            self.mon_resolution[0] // 2 - self.size[0] // 2, self.mon_resolution[1] // 2 - self.size[1] // 2)
        self.fps = 240
        os.environ['SDL_VIDEO_CENTERED'] = '0'

        self.bg_color = pygame.Color('black')
        self.image = pygame.image.load('images/Textures/Player.png')

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('WindowKill')
        pygame.display.set_icon(self.image)
        self.clock = pygame.time.Clock()
        self.window = Window.from_display_module()

        # Экземпляры классов
        self.player = Player(self)
        self.timer = Timer()
        self.health = Health(self.player.health)

        self.status = 'none'
        self.time = 0

    def update(self):
        # Обновление экрана каждый кадр
        self.screen.fill(self.bg_color)
        self.resize_window_minus()
        self.player.bullets.draw()
        draw_particles(self.screen)
        draw_enemys(self.screen)
        self.player.draw()
        self.timer.draw(self)
        self.player.coins.draw(self)
        self.health.draw(self)
        pygame.display.update()
        self.clock.tick(self.fps)

    def resize_window_minus(self):
        # Уменьшает окно каждый кадр
        if self.width > self.min_size[0]:
            if self.status != 'right':
                self.width -= 0.125
            if self.status != 'left':
                self.x += 0.125
                self.width -= 0.125
            if self.status == 'none':
                self.width -= 0.125
                self.x += 0.0625
        if self.height > self.min_size[1]:
            if self.status != 'down':
                self.height -= 0.125
            if self.status != 'up':
                self.y += 0.125
                self.height -= 0.125
            if self.status == 'none':
                self.height -= 0.125
                self.y += 0.0625
        self.pos = int(self.x), int(self.y)
        self.size = int(self.width), int(self.height)
        self.window.size = self.size
        self.window.position = self.pos
        if self.status != 'none':
            self.time += 1
            if self.time >= 480:
                self.time = 0
                self.status = 'none'

    def resize_window_plus(self, pos, punching):
        # Увеличивает окно при соприкосновении с ним пули
        if pos[0] - self.x <= 0:
            self.status = 'left'
            if self.x - 200 <= 0:
                self.x -= punching * max(self.x / 200, 0)
                self.width += punching * max(self.x / 200, 0)
            else:
                self.x -= punching
                self.width += punching
        if pos[1] - self.y <= 0:
            self.status = 'up'
            if self.y - 150 <= punching:
                self.y -= punching * max((self.y - punching) / 150, 0)
                self.height += punching * max((self.y - punching) / 150, 0)
            else:
                self.y -= punching
                self.height += punching
        if pos[0] - self.x >= self.size[0]:
            self.status = 'right'
            if (self.x + self.size[0]) + 200 >= self.mon_resolution[0]:
                self.width += punching * max((1 - ((self.x + self.size[0]) - self.mon_resolution[0] + 200) / 200), 0)
            else:
                self.width += punching
        if pos[1] - self.y >= self.size[1]:
            self.status = 'down'
            if (self.y + self.size[1]) + 200 >= self.mon_resolution[1]:
                self.height += punching * max((1 - ((self.y + self.size[1] + 50) - self.mon_resolution[1] + 150) / 150),
                                              0)
            else:
                self.height += punching
        self.size = int(self.width), int(self.height)
        self.pos = int(self.x), int(self.y)
        self.window.size = self.size
        self.window.position = self.pos

    def clear(self):
        # Очищает координаты и позицию окна
        self.size = self.width, self.height = (500, 500)
        self.pos = self.x, self.y = (
            self.mon_resolution[0] // 2 - self.size[0] // 2, self.mon_resolution[1] // 2 - self.size[1] // 2)

        self.status = 'none'
        self.time = 0
