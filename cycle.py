import pygame.event

from screen import *
from ui import StartWindow
from read_files import read_settings


class App:
    def __init__(self):
        self.buttonsPressed = []
        self.run = True

        self.screen = Screen(self)

    def checkEvents(self):
        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.buttonsPressed.append(event.key)
            if event.type == pygame.KEYUP:
                self.buttonsPressed.remove(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.screen.player.bullets.shoot(pygame.mouse.get_pos())

    def Run(self):
        # Основной цикл
        # sound = r'sounds\fon_music_2.wav'
        # pygame.mixer.Sound(sound).play(0, -1, False)
        # pygame.
        while self.run:
            self.checkEvents()
            self.screen.player.move(self.buttonsPressed)
            self.screen.player.update()
            self.screen.player.bullets.update()
            in_tamer_on_off, hide_HUD_on_off = read_settings()[2:]
            self.screen.timer.update(in_tamer_on_off)
            self.screen.player.coins.update(hide_HUD_on_off)
            self.screen.health.update(self.screen.player.health, self.screen.player.maxHealth, hide_HUD_on_off)
            updateEnemys(self.screen)
            updateParticlesXP(self.screen.player)
            updateParticlesShoot()
            updateParticlesDamage()
            self.screen.update()

    def clear(self):
        self.buttonsPressed = []
        self.screen.clear()
        self.screen.timer.clear()
        self.screen.player.clear()
        self.screen.player.coins.clear()
        self.screen.health.clear()
        self.screen.player.bullets.clear()
        clearEnemies()
        clearParticles()


if __name__ == '__main__':
    app = App()
    app.Run()
