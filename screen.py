import os

from screeninfo import get_monitors

from player import Player
from enemys import *


class Screen:
    def __init__(self, parent=None):
        # Настройки окна
        self.parent = parent
        self.minSize = (300, 300)
        self.size = self.width, self.height = (800, 800)
        self.monResolution = self.getMonitorResolution()
        self.pos = self.x, self.y = (
            self.monResolution[0] // 2 - self.size[0], self.monResolution[1] // 2 - self.size[1])
        self.fps = 120

        self.bgColor = pygame.Color('black')
        self.image = pygame.image.load('images/Player.png')

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('WindowKill')
        pygame.display.set_icon(self.image)
        self.clock = pygame.time.Clock()

        # Экземпляры классов
        self.player = Player(self)

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
            self.width -= 0.25
        if self.height > self.minSize[1]:
            self.height -= 0.25
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        # erguohdfbnosdvnidefjlbrwieeegknkvnadjkbnaknve;adsi2u9ipwegu9q3jkpowrrrhtnhr
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)

    def resizeWindowPlus(self, pos):
        # Увеличивает окно при соприкосновении с ним пули
        if pos[0] <= 0:
            pass
        if pos[1] <= 0:
            pass
        if pos[0] >= self.size[0]:
            self.width += 30
        if pos[1] >= self.size[1]:
            self.height += 30
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
