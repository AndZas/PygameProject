import sys
import pygame
import os


class StartWidndow:
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

        self.off_sound = 1

    def draw(self):
        path = 'images\StartWindow'

        # Надпись WindowKill
        font = pygame.font.Font(None, 100)
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
        if self.off_sound == 1:
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
        x, y = mouse_pos
        if self.pos_play[0] < x < self.pos_play[0] + self.play_w and self.pos_play[1] < y < self.pos_play[
            1] + self.play_h:
            self.play_game = True
            print('Играть')
        elif self.pos_settings[0] < x < self.pos_settings[0] + self.settings_w and \
                self.pos_settings[1] < y < self.pos_settings[1] + self.settings_h:
            self.open_menu()
        elif self.pos_dynamic[0] < x < self.pos_dynamic[0] + self.dynamic_w and \
                self.pos_dynamic[1] < y < self.pos_dynamic[1] + self.dynamic_h:
            self.off_sound *= -1  # -1 - выключить 1 - включить
        elif self.pos_door[0] < x < self.pos_door[0] + self.door_w and \
                self.pos_door[1] < y < self.pos_door[1] + self.door_h:
            sys.exit()

    def open_menu(self):
        menu = Menu(self.screen)
        run = True
        clock = pygame.time.Clock()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
            menu.run()
            pygame.display.flip()
            clock.tick(60)


class Menu:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.sliders = [Slider((400, 35), (200, 10), 0.5, 0, 100), Slider((400, 75), (200, 10), 0.5, 0, 100),
                        SwitchButton((300, 105), False), SwitchButton((300, 150), False)]
        self.texts = [Text((105, 20), 40, 'sound effect'), Text((190, 60), 40, 'music'),
                      Text((85, 105), 40, 'in-game timer'), Text((145, 155), 40, 'hide HUD')]

    def run(self):
        self.screen.fill("black")

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
    def __init__(self, pos: tuple, size: tuple, text: str):
        self.pos = pos
        self.size = size
        self.text = text

    def render(self, screen):
        font = pygame.font.Font(None, self.size)
        text = font.render(self.text, 1, (255, 255, 255))
        screen.blit(text, (self.pos))


class SwitchButton:
    def __init__(self, pos: tuple, working=False):
        self.pos = pos
        self.working = working
        self.w = 60
        self.h = 30
        self.container_rect = pygame.Rect(pos[0], pos[1], pos[0] + self.w, pos[1] + self.h)

    def render(self, screen):
        if self.working:
            img = pygame.transform.scale(pygame.image.load('images\StartWindow\on_btn.png'), (self.w, self.h))
        else:
            img = pygame.transform.scale(pygame.image.load('images\StartWindow\off_btn.png'), (self.w, self.h))
        screen.blit(img, (self.pos))  # левый верхний угол в точке pos

    def __str__(self):
        return 'SwitchButton'


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    running = True
    w = StartWidndow(screen)
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


if __name__ == '__main__':
    main()
