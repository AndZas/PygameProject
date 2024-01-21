import pygame.event

from screen import *
from ui import StartWindow, SpaceWindow
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
                if event.key == pygame.K_SPACE:
                    app = SpaceWindow(self.screen.screen)
                    running3 = True
                    while running3:
                        for event2 in pygame.event.get():
                            if event2.type == pygame.KEYDOWN and event2.key == pygame.K_SPACE:
                                running3 = False
                            elif event2.type == pygame.MOUSEBUTTONDOWN and event2.button == 1:
                                app.click()
                        app.run()
                        pygame.display.update()
                        self.screen.window.position = (self.screen.monResolution[0] // 2 - 600 // 2,
                                                       self.screen.monResolution[1] // 2 - 400 // 2)
                        self.screen.window.size = (600, 400)
                else:
                    self.buttonsPressed.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key != pygame.K_SPACE:
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
            in_tamer_on_off, hide_HUD_on_off = read_settings()[2:4]
            self.screen.timer.update(in_tamer_on_off)
            self.screen.player.coins.update(hide_HUD_on_off)
            self.screen.health.update(self.screen.player.health, self.screen.player.maxHealth, hide_HUD_on_off)
            updateEnemys(self.screen)
            updateParticlesXP(self.screen.player)
            updateParticles()
            self.screen.update()

    def clear(self):
        # Очистка всех данных для перезапуска
        self.buttonsPressed = []
        self.screen.clear()
        self.screen.timer.clear()
        self.screen.player.clear()
        self.screen.player.coins.clear()
        self.screen.health.clear()
        self.screen.player.bullets.clear()
        clearEnemies()
        clearParticles()
        dump_money_and_health(0, 10)
        dump_json_file()


if __name__ == '__main__':
    app = App()
    app.Run()
