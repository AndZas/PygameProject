from screen import *
from read_files import *


class App:
    def __init__(self):
        self.buttonsPressed = []
        self.run = True
        self.screen = Screen(self)

    def Run(self):
        if self.screen.clear_:
            self.clear()
            self.screen.clear_ = False
        self.screen.player.move(self.buttonsPressed)
        self.screen.player.update()
        self.screen.player.bullets.update()
        tamer_on_off, HUD_on_off = read_settings()[2:4]
        self.screen.timer.update(tamer_on_off)
        self.screen.player.coins.update(hide_HUD_on_off)
        self.screen.health.update(self.screen.player.health, self.screen.player.maxHealth, HUD_on_off)
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