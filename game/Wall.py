import pygame

from core.Config import Config

class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być tuplą 3 liczb całkowitych w zakresie 0–255 (RGB)"

        self.rect = pygame.Rect(x, y, width * Config.SCALE_X, height * Config.SCALE_Y)
        self.color = color

    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        pygame.draw.rect(screen, self.color, self.rect)
