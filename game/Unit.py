import pygame

from game_engine import GameEngine
from core.Config import Config

class Unit(pygame.sprite.Sprite):
    def __init__(self, coordinates: pygame.math.Vector2, engine: GameEngine, unit_color: tuple[int, int, int] = Config.UNIT_COLOR):
        assert isinstance(coordinates, pygame.math.Vector2), "coordinates musi być pygame.math.Vector2"
        assert isinstance(engine, GameEngine), "engine musi być instancją GameEngine"
        assert isinstance(engine.step, int) and engine.step > 0, "engine.step musi być dodatnią liczbą całkowitą"
        assert isinstance(unit_color, tuple) and len(unit_color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in unit_color), "unit_color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        super().__init__()
        unit_size = engine.step
        self.image = pygame.Surface((unit_size - 3, unit_size - 3))
        self.image.fill(unit_color)
        self.rect = self.image.get_rect(topleft=coordinates)

    def update(self, new_pos):
        assert isinstance(new_pos, pygame.math.Vector2), "new_pos musi być pygame.math.Vector2"
        self.rect.topleft = new_pos
