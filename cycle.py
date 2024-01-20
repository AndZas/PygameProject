import pygame.event

from screen import *


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
        while self.run:
            self.checkEvents()
            self.screen.player.move(self.buttonsPressed)
            self.screen.player.update()
            self.screen.player.bullets.update()
            self.screen.timer.update(True)
            self.screen.player.coins.update(True)
            self.screen.health.update(self.screen.player.health, self.screen.player.maxHealth, True)
            updateEnemys(self.screen)
            updateParticlesXP(self.screen.player)
            updateParticlesShoot()
            updateParticlesDamage()
            self.screen.update()

    def clear(self):
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
