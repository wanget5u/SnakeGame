import pygame

from core.Config import Config

class Tile:
    def __init__(self, x: int, y: int, size: int, color: tuple[int, int, int]):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(size, (int, float)) and size > 0, "size musi być dodatnią liczbą"
        assert isinstance(color, tuple) and len(color) == 3, "color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        self.rect = pygame.Rect(x, y, size, size)
        self.color = color

    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        pygame.draw.rect(screen, self.color, self.rect)
