import pygame
from read_files import load_img, load_font


# Быстрое создание надписей
class Text:
    def __init__(self, pos: tuple, size: int, text: str, center_x: bool = False, color: tuple = (255, 255, 255)):
        self.pos = pos
        self.size = size
        self.text = text
        self.center_x = center_x
        self.color = color

    # Рендер
    def render(self, screen):
        font = load_font(r'Font\Comfortaa-VariableFont_wght.ttf', self.size)
        text = font.render(self.text, 1, self.color)

        if self.center_x:
            self.pos = [screen.get_width() // 2 - text.get_width() // 2, self.pos[1]]
        screen.blit(text, self.pos)


# Создание плиток уровней
class Level:
    def __init__(self, pos: tuple, size: tuple, text='', lvl_done=None):
        self.x, self.y = pos
        self.w, self.h = size
        self.text = text
        self.color = (0, 255, 0)
        if int(self.text) < lvl_done:
            self.color = (181, 230, 29)
        self.container_rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def get_level(self):
        # Возвращает выбранный уровень
        return int(self.text)

    def render(self, screen):
        # Отрисовка
        pygame.draw.rect(screen, color=self.color, rect=self.container_rect)
        font = pygame.font.Font(None, 100)
        text = font.render(self.text, 1, (255, 255, 255))
        text_x = self.x + self.w // 2 - text.get_width() // 2
        text_y = self.y + self.h // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def __str__(self):
        return 'Level'


# Создание переключателя
class SwitchButton:
    def __init__(self, pos: tuple, working: bool = False, text: str = ''):
        self.pos = pos
        self.working = working
        self.w = 60
        self.h = 40
        self.text = text
        self.container_rect = pygame.Rect(pos[0], pos[1], self.w, self.h)

    def render(self, screen):
        # Отрисовка
        if self.working:
            img = load_img(r'images\StartWindow\on_btn.png', self.w, self.h)
        else:
            img = load_img(r'images\StartWindow\off_btn.png', self.w, self.h)
        screen.blit(img, self.pos)  # левый верхний угол в точке pos

    def get_name(self):
        # Возвращает текст
        return self.text

    def __str__(self):
        return 'SwitchButton'


# Создание слайдера
class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min_: int, max_: int) -> None:
        self.pos = pos
        self.size = size
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)
        self.initial_val = initial_val
        self.min = min_
        self.max = max_
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos - 5, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val, pos[1], 10,
                                       self.size[1])

    def move_slider(self, mouse_pos):
        # Изменить позицию слайдера
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def render(self, screen):
        # Отрисовка
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
        # Возвращает значение слайдера
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def __str__(self):
        return 'Slider'


# Загрузка изображений
class Image:
    def __init__(self, path: str, size: tuple, pos: tuple):
        self.path = path
        self.w, self.h = size
        self.pos = pos
        self.container_rect = pygame.Rect(pos[0], pos[1], self.w, self.h)

    def render(self, screen):
        # Отрисовка
        speed = pygame.transform.scale(pygame.image.load(self.path), (self.w, self.h))
        screen.blit(speed, self.pos)

    def __str__(self):
        return 'Image'


# Быстрое создание надписей
class NextLevelNotification:
    def __init__(self, pos: tuple, size: int, text: str, color: tuple = (255, 255, 255)):
        self.pos = pos
        self.size = size
        self.color = color
        font = load_font(r'Font\Comfortaa-VariableFont_wght.ttf', self.size)
        self.text = font.render(text, 1, self.color)
        self.container_rect = pygame.Rect(pos[0], pos[1], self.text.get_width(), self.text.get_height())

    # Рендер
    def render(self, screen):
        screen.blit(self.text, self.container_rect)

    def __str__(self):
        return 'NextLevelNotification'
