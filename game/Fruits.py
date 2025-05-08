from random import choice

import pygame

from core.Config import Config
from game.EffectsManager import EffectsManager
from game_engine import GameEngine

class Fruits(pygame.sprite.Sprite):
    def __init__(self, position: pygame.math.Vector2, engine: GameEngine):
        assert isinstance(position, pygame.math.Vector2), "position musi być pygame.math.Vector2"
        assert isinstance(engine, GameEngine), "engine musi być instancją GameEngine"
        assert isinstance(engine.step, int) and engine.step > 0, "engine.step musi być dodatnią liczbą całkowitą"
        assert isinstance(Config.FRUIT_COLOR, tuple) and len(Config.FRUIT_COLOR) == 3 and all(
            isinstance(c, int) and 0 <= c <= 255 for c in Config.FRUIT_COLOR), "FRUIT_COLOR musi być krotką 3 liczb całkowitych z zakresu 0-255"

        super().__init__()
        size = engine.step
        self.image = pygame.Surface((size - 3, size - 3))
        self.effect = choice(choice(EffectsManager.ALL_EFFECTS))
        self.image.fill(Config.FRUIT_COLOR)
        self.rect = self.image.get_rect(topleft=position)
