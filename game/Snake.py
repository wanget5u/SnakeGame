import pygame

from game_engine.GameEngine import Direction
from game.Unit import Unit

"""
Klasa reprezentująca węża w grze.

Zarządza ruchem, rysowaniem, inicjalizacją i aktualizacją pozycji węża.
Współpracuje z silnikiem gry, który dostarcza logikę poruszania się,
inicjalizacji i kolizji.
"""
class Snake:
    def __init__(self, engine):
        self.engine = engine
        self.START_POS = None
        self.PREV_POS = None
        self.NEW_POS = None
        self.body = None  # Grupa sprite'ów reprezentujących ciało węża
        self.length = None
        self.direction = Direction.RIGHT  # Domyślny kierunek ruchu węża

    """Inicjalizuje ciało węża na podstawie pozycji startowej. Tworzy segmenty dla każdej części węża."""
    def initialize_body(self):
        self.body = pygame.sprite.Group()
        self.length = self.engine.get_initial_snake_length()

        for x in range(self.length):
            self.body.add(Unit(pygame.math.Vector2(self.START_POS[x]), self.engine))

    """Dodaje nowy segment (unit) do węża, np. po zjedzeniu owocu."""
    def add_unit(self, position: list[tuple[int, int]]):
        self.body.add(Unit(pygame.math.Vector2(position), self.engine))

    """Ustawia pozycję początkową węża, pobiera dane z silnika gry i inicjalizuje startowe współrzędne."""
    def set_start_pos(self):
        self.START_POS = self.engine.initialize_snake()
        self.PREV_POS = self.START_POS.copy()
        self.NEW_POS = self.START_POS.copy()

    """Rysuje węża na ekranie."""
    def render(self, screen):
        self.body.draw(screen)

    """Aktualizuje pozycję węża — przemieszcza wszystkie segmenty w kierunku obecnego ruchu."""
    def update(self):
        # Wyznacz nową pozycję na podstawie aktualnego kierunku
        self.NEW_POS = self.engine.move_snake(self.PREV_POS, self.direction)

        # Przesuwanie każdego segmentu ciała węża
        for unit, pos in zip(self.body.sprites(), self.NEW_POS):
            unit.update(pygame.math.Vector2(pos))

        self.PREV_POS = self.NEW_POS.copy()