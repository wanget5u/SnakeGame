import pygame

from core import Config
from ui.Label import Label

class Score:
    def __init__(self, x: int, y: int, text: str = "", size: int = Config.FONT_SIZE, score_x_offset: int = 200):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(size, (int, float)) and size > 0, "size musi być dodatnią liczbą"
        assert isinstance(score_x_offset, int), "score_x_offset musi być liczbą całkowitą"

        self.value = 0
        self.text = text
        self.score_label_title = Label(x, y, text, size)
        self.score_label = Label(x + score_x_offset, y, str(self.value), size)

    """Wyświetlanie licznika punktów."""
    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"
        self.score_label_title.draw(screen)
        self.score_label.draw(screen)

    """Dodawanie wartości do licznika punktów."""
    def add(self, value: int):
        assert isinstance(value, (int, float)), "value musi być liczbą"
        self.value += value
        self.score_label.text = str(self.value)

    """Ustawianie licznika na wartość."""
    def set_value(self, value):
        self.value = value
        self.score_label.text = str(value)