import pygame.event

from screen import *


class App:
    def __init__(self):
        self.buttonsPressed = []
        self.run = True

        self.screen = Screen()

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
            self.screen.player.bullets.update()
            updateEnemys(self.screen.player)
            updateParticlesXP(self.screen.player)
            self.screen.update()


if __name__ == '__main__':
    app = App()
    app.Run()
