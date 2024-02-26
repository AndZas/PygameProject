import sys
import time

import pygame
from widgets import Text, Level, Slider, SwitchButton, Image
from read_files import (read_json_file, dump_json_file,
                        read_money_and_health, dump_money_and_health,
                        dump_lvl, read_lvl, read_settings, restart_lvl)
from cycle import *
from screen import *

music_volume = None
sounds_effect = None
off_sound = 1
in_tamer_on_off = False
hide_HUD_on_off = True


# Создание стартового окна
class StartWindow:
    def __init__(self, screen):
        self.bg_music = None
        self.screen = screen
        self.play_w, self.play_h = 60, 60
        self.settings_w, self.settings_h = 30, 30
        self.dynamic_w, self.dynamic_h = 30, 30
        self.door_w, self.door_h = 30, 30
        self.pos_play = []
        self.pos_settings = [10, 10]
        self.pos_dynamic = [50, 10]
        self.pos_door = []

        self.play_background_music()
        pygame.display.set_caption('WindowKill')
        pygame.display.set_icon(pygame.image.load(r'images/Textures/Player.png'))

    def play_background_music(self):
        # Проигрывает фоновую музыку
        bg_music_file = r'sounds/fon_music_2.wav'
        self.bg_music = pygame.mixer.Sound(bg_music_file)
        self.bg_music.play(-1, -1, False)

    def on_off_volume_fon_music(self):
        # функция проверяет выключена музыка или нет и выставляет громкость
        if off_sound == 1:
            self.bg_music.set_volume(0.5)
        elif off_sound == -1:
            self.bg_music.set_volume(0)
        if music_volume is not None:
            self.bg_music.set_volume(music_volume)

    def draw(self):
        # Отрисовка стартового окна
        path = 'images/StartWindow'

        # Корректируем громкость
        self.on_off_volume_fon_music()

        # Надпись WindowKill
        font = pygame.font.Font('Font/Comfortaa-VariableFont_wght.ttf', 70)
        text = font.render("WindowKill", 1, (255, 255, 255))
        text_x = self.screen.get_width() // 2 - text.get_width() // 2
        text_y = self.screen.get_height() // 2 - text.get_height() // 2 - self.play_h - 10
        self.screen.blit(text, (text_x, text_y))

        # Кнопка play
        x, y = self.screen.get_width() // 2 - self.play_w // 2, self.screen.get_height() // 2 - self.play_h // 2 + 40
        Image(path + '/play_button.png', (self.play_w, self.play_h), (x, y)).render(self.screen)
        self.pos_play = [x, y, self.play_w, self.play_h]

        # Кнопка настроек
        Image(path + '/settings_4.png', (self.settings_w, self.settings_h), self.pos_settings).render(self.screen)

        # Кнопка динамика
        if off_sound == 1:
            dynamic = Image(path + '/dynamic.png', (self.dynamic_w, self.dynamic_h), self.pos_dynamic)
        else:
            dynamic = Image(path + r'/off_dynamic.png', (self.dynamic_w, self.dynamic_h), self.pos_dynamic)

        dynamic.render(self.screen)  # левый верхний угол в точке 50 10

        # Кнопка двери
        self.pos_door = [10, self.screen.get_height() - 40]
        x, y = self.pos_door
        door = Image(path + '/go_out.png', (self.door_w, self.door_h), (x, y))
        door.render(self.screen)

        with open('files_txt_json_db/settings', 'w') as file:  # добавить лвл
            file.write(f'{sounds_effect if sounds_effect is not None else 0.5};'
                       f'{music_volume if music_volume is not None else 0.5};'
                       f'{in_tamer_on_off};{hide_HUD_on_off}')

    def click(self, mouse_pos):
        # При нажатии на кнопку мыши срабатывает эта функция
        global off_sound, music_volume, sounds_effect
        x, y = mouse_pos
        if self.pos_play[0] < x < self.pos_play[0] + self.play_w \
                and self.pos_play[1] < y < self.pos_play[1] + self.play_h:
            pygame.time.delay(100)
            key = self.open_level_menu()

            if key:  # если выбрали уровень открываем окно игры
                app1 = App()
                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or app1.screen.flag is False:
                            run = False
                            app1.screen.flag = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                app2 = SpaceWindow(self.screen)
                                running3 = True
                                while running3:
                                    for event2 in pygame.event.get():
                                        if event2.type == pygame.KEYDOWN and event2.key == pygame.K_SPACE:
                                            running3 = False
                                        elif event2.type == pygame.MOUSEBUTTONDOWN and event2.button == 1:
                                            app2.click()
                                    app2.run()
                                    pygame.display.update()
                                    app1.screen.window.position = (app1.screen.monResolution[0] // 2 - 600 // 2,
                                                                   app1.screen.monResolution[1] // 2 - 400 // 2)
                                    app1.screen.window.size = (600, 400)
                                app1.buttonsPressed = []
                            else:
                                app1.buttonsPressed.append(event.key)
                        if event.type == pygame.KEYUP:
                            if event.key != pygame.K_SPACE:
                                if event.key in app1.buttonsPressed:
                                    app1.buttonsPressed.remove(event.key)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                app1.screen.player.bullets.shoot(pygame.mouse.get_pos())
                    app1.Run()
                app1.clear()
                pygame.display.set_mode((600, 400))
        elif self.pos_settings[0] < x < self.pos_settings[0] + self.settings_w and \
                self.pos_settings[1] < y < self.pos_settings[1] + self.settings_h:
            self.open_menu_settings()
        elif self.pos_dynamic[0] < x < self.pos_dynamic[0] + self.dynamic_w and \
                self.pos_dynamic[1] < y < self.pos_dynamic[1] + self.dynamic_h:
            if off_sound == 1:
                music_volume = 0
                sounds_effect = 0
            else:
                music_volume = 0.5
                sounds_effect = 0.5
            off_sound *= -1  # -1 - выключить 1 - включить
        elif self.pos_door[0] < x < self.pos_door[0] + self.door_w and \
                self.pos_door[1] < y < self.pos_door[1] + self.door_h:
            sys.exit()

    def open_menu_settings(self):
        # Открывает настройки
        menu = MenuSettings(self.screen, self.bg_music)
        run = True
        clock = pygame.time.Clock()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            menu.run()
            pygame.display.flip()
            clock.tick(60)

    def open_level_menu(self):
        # Открывает меню уровней
        menu = LevelsMenu(self.screen)
        run2 = True
        clock = pygame.time.Clock()
        key = False
        while run2:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or menu.lvl is not None:
                    if menu.lvl is not None:
                        key = True
                    run2 = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            menu.run()
            pygame.display.flip()
            clock.tick(60)
        return key


def ms_to_time(millis):
    seconds = (millis / 1000) % 60
    seconds = round(float(seconds), 2)
    minutes = int((millis / (1000 * 60)) % 60)
    hours = int((millis / (1000 * 60 * 60)) % 24)
    return f"{hours}:{minutes}:{seconds}"


# Финальное окно
class EndWindow:
    def __init__(self, screen, coins_collected: int, time_survived: str, bullets_fired: int, enemies_killed: int):
        self.screen = screen
        self.time_survived = ms_to_time(time_survived)
        self.texts = [Text((0, 40), 60, 'game over', center_x=True),
                      Text((0, 110 + 10), 25, f'coins collected: {coins_collected}', center_x=True),
                      Text((0, 155 + 13), 25, f'time survived: {self.time_survived}', center_x=True),
                      Text((0, 202 + 15), 25, f'bullets fired: {bullets_fired}', center_x=True),
                      Text((0, 250 + 17), 25, f'enemies killed: {enemies_killed}', center_x=True),
                      Text((0, 295 + 20), 15, f'close this window to try again', center_x=True, color=(143, 145, 168))]

    def run(self):
        # Рисует финальное окно
        for text in self.texts:
            text.render(self.screen)


# Окно настроек
class MenuSettings:
    def __init__(self, screen, music) -> None:
        self.screen = screen
        self.bg_music = music
        self.sound_effect = Slider((400, 35), (200, 10), sounds_effect if sounds_effect is not None else 0.5, 0, 100)
        self.music = Slider((400, 75), (200, 10), music_volume if music_volume is not None else 0.5, 0, 100)
        self.in_game_timer = SwitchButton((300, 100), in_tamer_on_off, text='in-game timer')
        self.hide_HUD = SwitchButton((300, 150), hide_HUD_on_off, text='hide HUD')
        self.sliders = [self.sound_effect, self.music, self.in_game_timer, self.hide_HUD]
        self.texts = [Text((105, 20), 25, 'sound effect'), Text((190, 60), 25, 'music'),
                      Text((85, 105), 25, 'in-game timer'), Text((145, 155), 25, 'hide HUD')]

    def change_music_effect_volume(self):
        # Изменяет громкость звуковых эффектов
        global music_volume, off_sound, sounds_effect
        music_volume = round(self.music.get_value() / 100, 1)
        sounds_effect = round(self.sound_effect.get_value() / 100, 1)
        if music_volume > 0:
            off_sound = 1
        self.bg_music.set_volume(music_volume)

    def run(self, event=None):
        # Рисует окно настроек
        global in_tamer_on_off, hide_HUD_on_off
        self.screen.fill("black")
        self.change_music_effect_volume()
        for i in self.texts:
            i.render(self.screen)

        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        print(mouse)
        for slider in self.sliders:
            if str(slider) == 'Slider':
                if slider.container_rect.collidepoint(mouse_pos):
                    if mouse[0]:
                        slider.grabbed = True
                if not mouse[0]:
                    slider.grabbed = False
                if slider.grabbed:
                    slider.move_slider(mouse_pos)
                slider.render(self.screen)
            elif str(slider) == 'SwitchButton':
                if slider.container_rect.collidepoint(mouse_pos) and mouse[0] == 1:
                    if slider.working is True:
                        if slider.get_name() == 'hide HUD':
                            hide_HUD_on_off = False
                        elif slider.get_name() == 'in-game timer':
                            in_tamer_on_off = False
                        slider.working = False
                    else:
                        if slider.get_name() == 'hide HUD':
                            hide_HUD_on_off = True
                        elif slider.get_name() == 'in-game timer':
                            in_tamer_on_off = True
                        slider.working = True
                    pygame.time.delay(100)
                slider.render(self.screen)


# Меню уровней
class LevelsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.lvl_done = read_lvl()
        self.levels = [Level((110, 100), (100, 100), '0', self.lvl_done),
                       Level((240, 100), (100, 100), '1', self.lvl_done),
                       Level((370, 100), (100, 100), '2', self.lvl_done),
                       Level((110, 230), (100, 100), '3', self.lvl_done),
                       Level((240, 230), (100, 100), '4', self.lvl_done),
                       Level((370, 230), (100, 100), '5', self.lvl_done)]
        self.text = Text((screen.get_width() // 2 - 220 // 2, 10), 65, 'Levels')
        self.lvl = None

    def run(self):
        # Рисует меню уровней
        self.screen.fill("black")
        self.text.render(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        for level in self.levels:
            if level.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    self.lvl = level.get_level()
                    dump_lvl(self.lvl)
                    pygame.time.delay(300)
            level.render(self.screen)


# Читает json файл
def read_json():
    data = read_json_file()
    money = read_money_and_health()[0]
    player_speed, player_wall_punch = data[0]
    player_hp = read_money_and_health()[1]
    speed_price, hp_price, wall_punch_price = data[1]
    return money, player_speed, player_wall_punch, player_hp, speed_price, hp_price, wall_punch_price


# Окно закупки
class SpaceWindow:
    def __init__(self, screen):

        self.speed = None
        self.heal = None
        self.wall_punch = None
        self.screen = screen
        self.w = 150
        self.h = 150
        self.money, self.pl_speed, self.pl_punch, self.pl_hp, self.speed_pr, self.hp_pr, self.punch_pr = read_json()

    def run(self):
        # Рисует окно закупки
        self.screen.fill("black")
        avr_sc_w = self.screen.get_width() // 2
        avr_w = self.w // 2

        pygame.draw.circle(self.screen, pygame.Color('Purple'), (avr_sc_w - 10, 50), 10)
        Text((avr_sc_w + 10, 35), 30, text=str(self.money), color=pygame.Color('Purple')).render(self.screen)

        x, y = avr_sc_w - avr_w - avr_w * 2 - 20, self.screen.get_height() // 2 - self.h // 2
        self.speed = Image('images/BuyMenuWindow/speed_img.png', (self.w, self.h), (x, y))
        self.speed.render(self.screen)
        pygame.draw.circle(self.screen, pygame.Color('Purple'), (avr_sc_w - avr_w * 2 - 30, 293), 5)
        Text((avr_sc_w - avr_w * 2 - 20, 280), 25, text=str(self.speed_pr), color=pygame.Color('Purple')).render(
            self.screen)

        x, y = avr_sc_w - avr_w, self.screen.get_height() // 2 - self.h // 2
        self.heal = Image('images/BuyMenuWindow/heal_img.png', (self.w, self.h), (x, y))
        self.heal.render(self.screen)
        pygame.draw.circle(self.screen, pygame.Color('Purple'), (avr_sc_w - 20, 293), 5)
        Text((0, 280), 25, text=str(self.hp_pr), color=pygame.Color('Purple'), center_x=True).render(self.screen)

        x, y = avr_sc_w - avr_w + avr_w * 2 + 20, self.screen.get_height() // 2 - self.h // 2
        self.wall_punch = Image('images/BuyMenuWindow/wall_punch.png', (self.w, self.h), (x, y))
        self.wall_punch.render(self.screen)
        pygame.draw.circle(self.screen, pygame.Color('Purple'), (avr_sc_w + avr_w * 2 + 11, 293), 5)
        Text((avr_sc_w + avr_w * 2 + 20, 280), 25, text=str(self.punch_pr),
             color=pygame.Color('Purple')).render(
            self.screen)

    def click(self):
        # обработчик события нажатия кнопки мыши
        mouse_pos = pygame.mouse.get_pos()
        if self.speed.container_rect.collidepoint(mouse_pos):
            if self.money >= self.speed_pr:
                self.pl_speed += 0.25
                self.money -= self.speed_pr
                self.speed_pr *= 2
        elif self.heal.container_rect.collidepoint(mouse_pos):
            if self.money >= self.hp_pr:
                self.pl_hp += 10
                self.money -= self.hp_pr
                self.hp_pr *= 2
        elif self.wall_punch.container_rect.collidepoint(mouse_pos):
            if self.money >= self.punch_pr:
                self.pl_punch += 10
                self.money -= self.punch_pr
                self.punch_pr *= 2

        pygame.time.delay(300)
        dct = {
            "Player": {"speed": self.pl_speed, "wall punch": self.pl_punch},
            "Prices": {"speed": self.speed_pr, "hp": self.hp_pr, "wall punch": self.punch_pr}}
        dump_json_file(dct)
        dump_money_and_health(money=self.money, health=min(10, self.pl_hp))
        read_json()
        self.money, self.pl_speed, self.pl_punch, self.pl_hp, self.speed_pr, self.hp_pr, self.punch_pr = read_json()
        self.run()


# Запуск приложения
def main1():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    running = True
    w = StartWindow(screen)
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                w.click(pos)
        w.draw()
        clock.tick(60)
        pygame.display.flip()


def main2(coins, time_2, bullets, enemys_2, parent):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    running2 = True
    w = EndWindow(screen, coins, time_2, bullets, enemys_2)
    clock = pygame.time.Clock()
    while running2:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False
        w.run()
        clock.tick(60)
        pygame.display.flip()
    parent.clear()


if __name__ == '__main__':
    dump_json_file()
    restart_lvl()
    dump_money_and_health(0, 10)
    main1()
