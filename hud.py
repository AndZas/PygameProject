import pygame
from read_files import read_money

pygame.init()


# Таймер
class Timer:
    def __init__(self):
        self.time = 0
        self.koef = 0.425
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)
        self.on = True

    # Отрисовка таймера
    def draw(self, screen):
        if self.on:
            screen.screen.blit(self.font.render(
                f'{int(self.time / 100 / 60 / 60) % 60}:{int(self.time / 100 / 60) % 60}:{int(self.time / 100) % 60}.'
                f'{int(self.time) % 100}',
                True, pygame.Color('Gray')), (10, screen.size[1] - 25))

    # Обновление таймера
    def update(self, on):
        self.on = on
        self.time += self.koef

    # Очистка таймера
    def clear(self):
        self.time = 0


# Опыт
class Coins:
    def __init__(self):
        self.count = read_money()
        self.on = True
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)

    # Отрисовка счетчика опыта
    def draw(self, screen):
        if self.on:
            pygame.draw.circle(screen.screen, pygame.Color('Purple'), (15, 15), 5)
            screen.screen.blit(self.font.render(str(self.count), True, pygame.Color('purple')), (25, 7))

    # Обновление счетчика опыта
    def update(self, on):
        self.count = read_money()
        self.on = on

    # Очистка опыта
    def clear(self):
        self.count = 0


# Счетчик здоровья
class Health:
    def __init__(self, hp=10):
        self.count = hp
        self.max = 10
        self.on = True
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)

    # Отрисовка счетчика здоровья
    def draw(self, screen):
        if self.on:
            text = self.font.render(str(f'HP:{self.count}/{self.max}'), True, pygame.Color('white'))
            screen.screen.blit(text, (screen.size[0] - text.get_width() - 5, 7))

    # Обновление счетчика здоровья
    def update(self, hp, maxHp, on):
        self.count = hp
        self.max = maxHp
        self.on = on

    # Очистка счетчика здоровья
    def clear(self):
        self.count = 10
        self.max = 10
