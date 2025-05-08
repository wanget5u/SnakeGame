import pygame
from random import choice

from game.EffectsManager import EffectsManager
from game_engine import GameEngine


class CollisionEffect(pygame.sprite.Sprite):
    def __init__(self, position: pygame.math.Vector2, engine: GameEngine):
        super().__init__()
        size = engine.step
        self.effect = choice(choice(EffectsManager.ALL_EFFECTS))

        try:
            self.image = pygame.image.load(self.effect.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (size - 3, size - 3))
        except Exception as e:
            print(f"⚠️ Nie udało się wczytać obrazka: {e}")
            # Fallback do koloru
            self.image = pygame.Surface((size - 3, size - 3))
            self.image.fill(self.effect.color)

        self.rect = self.image.get_rect(topleft=position)

    def trigger(self):
        self.effect.execute()

    def revert(self):
        self.effect.revert()