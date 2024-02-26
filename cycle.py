from screen import *
from read_files import *


class App:
    def __init__(self):
        self.buttons_pressed = []
        self.run = True
        self.screen = Screen(self)

    def run2(self):
        if self.screen.clear_:
            self.clear()
            self.screen.clear_ = False
        self.screen.player.move(self.buttons_pressed)
        self.screen.player.update()
        self.screen.player.bullets.update()
        tamer_on_off, HUD_on_off = read_settings()[2:4]
        self.screen.timer.update(tamer_on_off)
        self.screen.player.coins.update(HUD_on_off)
        self.screen.health.update(self.screen.player.health, self.screen.player.maxHealth, HUD_on_off)
        update_enemys(self.screen)
        update_particles_xp(self.screen.player)
        update_particles()
        self.screen.update()

    def clear(self):
        # Очистка всех данных для перезапуска
        self.buttons_pressed = []
        self.screen.clear()
        self.screen.timer.clear()
        self.screen.player.clear()
        self.screen.player.coins.clear()
        self.screen.health.clear()
        self.screen.player.bullets.clear()
        clear_enemies()
        clear_particles()
        dump_money_and_health(0, 10)
        dump_json_file()