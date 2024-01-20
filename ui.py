import sys
import pygame
import os

music_volume = None
sounds_effect = None
off_sound = 1


class StartWindow:
    def __init__(self, screen):
        self.screen = screen
        self.play_w, self.play_h = 60, 60
        self.settings_w, self.settings_h = 30, 30
        self.dynamic_w, self.dynamic_h = 30, 30
        self.door_w, self.door_h = 30, 30
        self.slider = Slider((screen.get_width() / 2, 100), (100, 30), 0.5, 0, 100)
        self.slider.render(screen)
        self.pos_play = []
        self.pos_settings = [10, 10]
        self.pos_dynamic = [50, 10]
        self.pos_door = []

        self.play_background_music()

    def play_background_music(self):
        bg_music_file = r'sounds\fon_music_2.wav'
        self.bg_music = pygame.mixer.Sound(bg_music_file)
        self.bg_music.play(0, -1, False)

    def on_off_volume_fon_music(self):  # функция проверяет выключена музыка или нет и выставляет громкость
        if off_sound == 1:
            self.bg_music.set_volume(0.5)
        elif off_sound == -1:
            self.bg_music.set_volume(0)
        if music_volume is not None:
            self.bg_music.set_volume(music_volume)

    def draw(self):
        path = 'images\StartWindow'

        # Корректируем громкость
        self.on_off_volume_fon_music()

        # Надпись WindowKill
        # text = Text((0, ))
        font = pygame.font.Font('Font\Comfortaa-VariableFont_wght.ttf', 70)
        text = font.render("WindowKill", 1, (255, 255, 255))
        text_x = self.screen.get_width() // 2 - text.get_width() // 2
        text_y = self.screen.get_height() // 2 - text.get_height() // 2 - self.play_h - 10
        self.screen.blit(text, (text_x, text_y))

        # Кнопка play
        play = pygame.transform.scale(pygame.image.load(path + '\play_button.png'),
                                      (self.play_w, self.play_h))
        x, y = self.screen.get_width() // 2 - self.play_w // 2, self.screen.get_height() // 2 - self.play_h // 2 + 40
        self.screen.blit(play, (x, y))
        self.pos_play = [x, y, self.play_w, self.play_h]

        # Кнопка настроек
        settings = pygame.transform.scale(pygame.image.load(path + '\settings_4.png'),
                                          (self.settings_w, self.settings_h))
        x, y = self.pos_settings
        self.screen.blit(settings, (x, y))  # левый верхний угол в точке 10 10

        # Кнопка динамика
        if off_sound == 1:
            dynamic = pygame.transform.scale(pygame.image.load(path + '\dynamic.png'), (self.dynamic_w, self.dynamic_h))
        else:
            dynamic = pygame.transform.scale(pygame.image.load(path + r'\off_dynamic.png'),
                                             (self.dynamic_w, self.dynamic_h))
        x, y = self.pos_dynamic
        self.screen.blit(dynamic, (x, y))  # левый верхний угол в точке 50 10

        # Кнопка двери
        door = pygame.transform.scale(pygame.image.load(path + '\go_out.png'),

                                      (self.door_w, self.door_h))
        self.pos_door = [10, self.screen.get_height() - 10 - door.get_height()]
        x, y = self.pos_door
        self.screen.blit(door, (x, y))

    def click(self, mouse_pos):
        global off_sound, music_volume, sounds_effect
        x, y = mouse_pos
        if self.pos_play[0] < x < self.pos_play[0] + self.play_w and self.pos_play[1] < y < self.pos_play[
            1] + self.play_h:
            self.play_game = True
            pygame.time.delay(100)
            self.open_level_menu()
            print('Играть')

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
        menu = MenuSettings(self.screen, self.bg_music)
        run = True
        clock = pygame.time.Clock()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            menu.run()
            pygame.display.flip()
            clock.tick(60)

    def open_level_menu(self):
        menu = LevelsMenu(self.screen)
        run2 = True
        clock = pygame.time.Clock()
        while run2:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run2 = False
            menu.run()
            pygame.display.flip()
            clock.tick(60)


class EndWindow():
    def __init__(self, screen, coins_collected: int, time_survived: str, bullets_fired: int, enemies_killed: int):
        '00:00:00'
        self.screen = screen
        self.texts = [Text((0, 40), 60, 'game over', center_x=True),
                      Text((0, 110 + 10), 25, f'coins collected: {coins_collected}', center_x=True),
                      Text((0, 155 + 13), 25, f'time survived: {time_survived}', center_x=True),
                      Text((0, 202 + 15), 25, f'bullets fired: {bullets_fired}', center_x=True),
                      Text((0, 250 + 17), 25, f'enemies killed: {enemies_killed}', center_x=True),
                      Text((0, 295 + 20), 15, f'close this window to try again', center_x=True, color=(143, 145, 168))]

    def run(self):
        for text in self.texts:
            text.render(self.screen)


class MenuSettings:
    def __init__(self, screen, music) -> None:
        self.screen = screen
        self.bg_music = music
        self.sound_effect = Slider((400, 35), (200, 10), sounds_effect if sounds_effect is not None else 0.5, 0, 100)
        self.music = Slider((400, 75), (200, 10), music_volume if music_volume is not None else 0.5, 0, 100)
        self.in_game_timer = SwitchButton((300, 100), False)
        self.hide_HUD = SwitchButton((300, 150), False)
        self.sliders = [self.sound_effect, self.music, self.in_game_timer, self.hide_HUD]
        self.texts = [Text((105, 20), 25, 'sound effect'), Text((190, 60), 25, 'music'),
                      Text((85, 105), 25, 'in-game timer'), Text((145, 155), 25, 'hide HUD')]

    def change_music_effect_volume(self):
        global music_volume, off_sound, sounds_effect
        music_volume = round(self.music.get_value() / 100, 1)
        sounds_effect = round(self.sound_effect.get_value() / 100, 1)
        if music_volume > 0:
            off_sound = 1
        self.bg_music.set_volume(music_volume)

    def run(self):
        self.screen.fill("black")
        self.change_music_effect_volume()
        for i in self.texts:
            i.render(self.screen)
        """///"""
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
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
                        slider.working = False
                    else:
                        slider.working = True
                    pygame.time.delay(100)
                slider.render(self.screen)
        """///"""


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)
        self.initial_val = initial_val
        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos - 5, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val, pos[1], 10,
                                       self.size[1])

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def render(self, screen):
        pygame.draw.rect(screen, (69, 76, 89), self.container_rect)
        x, y, w, h = self.container_rect

        pygame.draw.rect(surface=screen, color='white', rect=(x, y, self.button_rect[0] - x, h))
        pygame.draw.circle(screen, 'black', (self.button_rect[0], self.button_rect[1]), 13)
        pygame.draw.circle(surface=screen, color='white', center=(self.button_rect[0], self.button_rect[1]), radius=10)
        if x <= self.button_rect[0]:
            color_left = 'white'
        else:
            color_left = (69, 76, 89)
        if x + w <= self.button_rect[0]:
            color_right = 'white'
        else:
            color_right = (69, 76, 89)
        pygame.draw.circle(screen, color_left, (x, self.button_rect[1]), 5)
        pygame.draw.circle(screen, color_right, (x + w, self.button_rect[1]), 5)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def __str__(self):
        return 'Slider'


class Text():
    def __init__(self, pos: tuple, size: tuple, text: str, center_x: bool = False, color: tuple = (255, 255, 255)):
        self.pos = pos
        self.size = size
        self.text = text
        self.center_x = center_x
        self.color = color

    def render(self, screen):
        font = pygame.font.Font('Font\Comfortaa-VariableFont_wght.ttf', self.size)
        text = font.render(self.text, 1, self.color)

        if self.center_x:
            self.pos = [screen.get_width() // 2 - text.get_width() // 2, self.pos[1]]
        screen.blit(text, (self.pos))


class SwitchButton:
    def __init__(self, pos: tuple, working=False):
        self.pos = pos
        self.working = working
        self.w = 60
        self.h = 40
        self.container_rect = pygame.Rect(pos[0], pos[1], self.w, self.h)

    def render(self, screen):
        if self.working:
            img = pygame.transform.scale(pygame.image.load('images\StartWindow\on_btn.png'), (self.w, self.h))
        else:
            img = pygame.transform.scale(pygame.image.load('images\StartWindow\off_btn.png'), (self.w, self.h))
        screen.blit(img, (self.pos))  # левый верхний угол в точке pos

    def __str__(self):
        return 'SwitchButton'


class LevelsMenu():
    def __init__(self, screen):
        self.screen = screen
        self.levels = [Level((110, 100), (100, 100), '0'), Level((240, 100), (100, 100), '1'),
                       Level((370, 100), (100, 100), '2'), Level((110, 230), (100, 100), '3'),
                       Level((240, 230), (100, 100), '4'), Level((370, 230), (100, 100), '5')]
        self.text = Text((screen.get_width() // 2 - 220 // 2, 10), 65, 'Levels')

    def run(self):
        self.screen.fill("black")
        self.text.render(self.screen)
        """///"""
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        for level in self.levels:
            if level.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    print(level.get_level())
                    pygame.time.delay(100)
            level.render(self.screen)
        """///"""


class Level():
    def __init__(self, pos: tuple, size: tuple, text=''):
        self.x, self.y = pos
        self.w, self.h = size
        self.text = text
        self.container_rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def get_level(self):
        return int(self.text)

    def render(self, screen):
        pygame.draw.rect(screen, color='green', rect=self.container_rect)
        font = pygame.font.Font(None, 100)
        text = font.render(self.text, 1, (255, 255, 255))
        text_x = self.x + self.w // 2 - text.get_width() // 2
        text_y = self.y + self.h // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def __str__(self):
        return 'Level'


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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                w.click(pos)
        w.draw()
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


def main2(coins, time):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    running = True
    w = EndWindow(screen, coins, time, 20, 2)
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                w.click(pos)
        w.run()
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main1()
