import os
from pygame._sdl2.video import Window
from screeninfo import get_monitors

from enemys import *
from player import Player


class Screen:
    def __init__(self, parent=None):
        # Настройки окна
        self.parent = parent
        self.minSize = (300, 300)
        self.size = self.width, self.height = (800, 800)
        self.monResolution = self.getMonitorResolution()
        self.pos = self.x, self.y = (
            self.monResolution[0] // 2 - self.size[0] // 2, self.monResolution[1] // 2 - self.size[1] // 2)
        self.fps = 120
        os.environ['SDL_VIDEO_CENTERED'] = '0'

        self.bgColor = pygame.Color('black')
        self.image = pygame.image.load('images/Player.png')

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('WindowKill')
        pygame.display.set_icon(self.image)
        self.clock = pygame.time.Clock()
        self.window = Window.from_display_module()

        # Экземпляры классов
        self.player = Player(self)

        #
        self.status = 'none'
        self.time = 0

    def getMonitorResolution(self):
        # Возвращает разрешение монитора
        for monitor in get_monitors():
            if monitor.is_primary:
                return (monitor.width, monitor.height)

    def update(self):
        # Обновление экрана каждый кадр
        self.screen.fill(self.bgColor)
        self.resizeWindowMinus()
        self.player.bullets.draw()
        drawParticlesXP(self.screen)
        drawEnemys(self.screen)
        self.player.draw()
        pygame.display.update()
        self.clock.tick(self.fps)

    def resizeWindowMinus(self):
        # Уменьшает окно каждый кадр
        if self.width > self.minSize[0]:
            if self.status != 'right':
                self.width -= 0.25
            if self.status != 'left':
                self.x += 0.25
                self.width -= 0.25
            if self.status == 'none':
                self.width -= 0.25
                self.x += 0.125
        if self.height > self.minSize[1]:
            if self.status != 'down':
                self.height -= 0.25
            if self.status != 'up':
                self.y += 0.25
                self.height -= 0.25
            if self.status == 'none':
                self.height -= 0.25
                self.y += 0.125
        self.pos = self.x, self.y
        self.size = self.width, self.height
        # self.screen = pygame.display.set_mode(self.size)
        self.window.size = self.size
        self.window.position = self.pos
        if self.status != 'none':
            self.time += 1
            if self.time >= 240:
                self.time = 0
                self.status = 'none'

    def resizeWindowPlus(self, pos):
        # Увеличивает окно при соприкосновении с ним пули
        if pos[0] <= 0:
            self.status = 'left'
            self.x -= 30
            self.width += 30
        if pos[1] <= 0:
            self.status = 'up'
            self.y -= 30
            self.height += 30
        if pos[0] >= self.size[0]:
            self.status = 'right'
            self.width += 30
        if pos[1] >= self.size[1]:
            self.status = 'down'
            self.height += 30
        self.size = self.width, self.height
        self.pos = self.x, self.y
        # self.screen = pygame.display.set_mode(self.size)
        self.window.size = self.size
        self.window.position = self.pos
