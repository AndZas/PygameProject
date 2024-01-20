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
        self.on = Timer

    def draw(self, screen):
        if self.on:
            screen.screen.blit(self.font.render(
                f'{int(self.time / 100 / 60 / 60)}:{int(self.time / 100 / 60)}:{int(self.time / 100)}.'
                f'{str(int(self.time))[max(int(len(str(int(self.time)))), 2) - 2:]}',
                True, pygame.Color('Gray')), (10, screen.size[1] - 25))

    def update(self, on):
        self.on = on
        self.time += self.koef
