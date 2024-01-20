import pygame

pygame.init()


class RedBorder:
    def __init__(self):
        self.timer = 0
        self.image = pygame.image.load('images/Textures/DamageBorder2.png')

    def draw(self, screen):
        # if 0 < self.timer <= 240:
        screen.screen.blit(pygame.transform.scale(self.image, screen.size), (0, 0))


class Timer:
    def __init__(self):
        self.time = 0
        self.koef = 0.425
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)
        self.on = True

    def draw(self, screen):
        if self.on:
            screen.screen.blit(self.font.render(
                f'{int(self.time / 100 / 60 / 60) % 60}:{int(self.time / 100 / 60) % 60}:{int(self.time / 100) % 60}.'
                f'{int(self.time) % 100}',
                True, pygame.Color('Gray')), (10, screen.size[1] - 25))

    def update(self, on):
        self.on = on
        self.time += self.koef

    def clear(self):
        self.time = 0


class Coins:
    def __init__(self):
        self.count = 0
        self.on = True
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)

    def draw(self, screen):
        if self.on:
            pygame.draw.circle(screen.screen, pygame.Color('Purple'), (15, 15), 5)
            screen.screen.blit(self.font.render(str(self.count), True, pygame.Color('purple')), (25, 7))

    def update(self, on):
        self.on = on

    def clear(self):
        self.count = 0


class Health:
    def __init__(self):
        self.count = 10
        self.max = 10
        self.on = True
        self.font = pygame.font.Font('font/AtariClassic-gry3.ttf', 15)

    def draw(self, screen):
        if self.on:
            text = self.font.render(str(f'HP:{self.count}/{self.max}'), True, pygame.Color('white'))
            screen.screen.blit(text, (screen.size[0] - text.get_width() - 5, 7))

    def update(self, hp, maxHp, on):
        self.count = hp
        self.max = maxHp
        self.on = on

    def clear(self):
        self.count = 10
        self.max = 10
