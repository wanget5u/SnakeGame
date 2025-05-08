import pygame.font

from core.Config import Config

class Label:
    def __init__(self, x: int, y: int,
                 text: str, font_size: int = Config.FONT_SIZE, text_color: tuple[int, int, int] = Config.TEXT_COLOR):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(font_size, (int, float)) and font_size > 0, "font_size musi być dodatnią liczbą"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"

        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color

        self.font = pygame.font.Font(None, int(font_size * Config.SCALE_Y))

    """Rysowanie tekstu na ekranie."""
    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    """Ustawienie tekstu labelu."""
    def set_text(self, text: str):
        assert isinstance(text, str), "tekst musi być typu str"
        self.text = text
