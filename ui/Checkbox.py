import pygame
from core.Config import Config

class Checkbox:
    def __init__(self, x: int, y: int, size: int,
                 text: str, color: tuple[int, int, int], text_color: tuple[int, int, int] = Config.TEXT_COLOR,
                 checked: bool = False):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(size, int) and size > 0, "size musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert all(isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color) for color in [color, text_color]), "kolory muszą być krotkami 3 liczb całkowitych z zakresu 0-255"

        # Tworzenie prostokąta checkboxa
        self.rect = pygame.Rect(x, y, size * Config.SCALE_X, size * Config.SCALE_Y)
        self.rect.center = (x * Config.SCALE_X, y * Config.SCALE_Y)

        # Tekst i kolory
        self.text = text
        self.color = color
        self.color_hover = tuple(min(255, int(c * 1.2)) for c in color)  # Kolor po najechaniu myszką
        self.color_click = tuple(min(255, int(c * 1.4)) for c in color)  # Kolor podczas kliknięcia
        self.check_color = tuple(int(x * 1.9) for x in color)  # Kolor wypełnienia zaznaczenia

        self.text_color = text_color
        self.font = pygame.font.SysFont(None, int(Config.FONT_SIZE * Config.SCALE_Y))

        self.checked = checked  # Stan zaznaczenia
        self.is_pressed = False  # Czy checkbox jest wciśnięty

    """Rysowanie checkboxa i tekstu na ekranie."""
    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        # Wybór koloru w zależności od stanu przycisku
        if self.is_pressed:
            current_color = self.color_click
        elif self.is_hovered():
            current_color = self.color_hover
        else:
            current_color = self.color

        # Rysowanie głównego prostokąta checkboxa
        pygame.draw.rect(screen, current_color, self.rect, border_radius=4)

        # Jeśli zaznaczony, rysuj mniejszy prostokąt w środku (symbol zaznaczenia)
        if self.checked:
            inner_rect = self.rect.inflate(-self.rect.width * 0.4, -self.rect.height * 0.4)
            pygame.draw.rect(screen, self.check_color, inner_rect, border_radius=3)

        # Rysowanie tekstu obok checkboxa
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 20, self.rect.centery))
        screen.blit(text_surface, text_rect)

    """Sprawdzanie, czy kursor znajduje się nad checkboxem."""
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    """Obsługa zdarzeń myszy dla checkboxa."""
    def handle_event(self, event, on_toggle=None):
        # Kliknięcie lewym przyciskiem myszy na checkbox
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered():
            self.is_pressed = True

        # Zwolnienie lewego przycisku myszy
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered():
                self.checked = not self.checked
                if callable(on_toggle):
                    on_toggle()  # Wywołanie funkcji po zmianie stanu (jeśli podana)
            self.is_pressed = False
