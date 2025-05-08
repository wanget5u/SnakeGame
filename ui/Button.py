import pygame
from core.Config import Config

class Button:
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, color: tuple[int, int, int], text_color: tuple[int, int, int] = Config.TEXT_COLOR, text_size: int = Config.FONT_SIZE,
                 preview_surface: pygame.surface.Surface = None):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_size, int) and text_size > 0, "text_size musi być nieujemną liczbą całkowitą"

        # Tworzenie prostokąta przycisku, skalowanego do obecnej rozdzielczości
        self.rect = pygame.Rect(x, y, width * Config.SCALE_X, height * Config.SCALE_Y)
        self.rect.center = (x * Config.SCALE_X, y * Config.SCALE_Y)

        # Ustawienia tekstu i kolorów
        self.text = text
        self.color = color
        self.color_hover = tuple(min(255, int(c * 1.2)) for c in color)  # Kolor przy najechaniu kursorem
        self.color_click = tuple(min(255, int(c * 1.4)) for c in color)  # Kolor przy kliknięciu
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, int(text_size * Config.SCALE_Y))

        # Stan przycisku
        self.is_pressed = False

        # Opcjonalne wyświetlanie presetu planszy zamiast tekstu na przycisku
        self.preview_surface = preview_surface

    """Rysowanie przycisku na ekranie."""
    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        # Wybór koloru przycisku w zależności od interakcji
        if self.is_pressed:
            current_color = self.color_click
        elif self.is_hovered():
            current_color = self.color_hover
        else:
            current_color = self.color

        # Rysowanie prostokąta przycisku
        pygame.draw.rect(screen, current_color, self.rect, border_radius=4)

        # Wyświetlanie presetu planszy albo tekstu
        if self.preview_surface:
            preview_rect = self.preview_surface.get_rect(center=self.rect.center)
            screen.blit(self.preview_surface, preview_rect)
        else:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    """Sprawdzanie, czy kursor znajduje się nad przyciskiem."""
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    """Obsługa zdarzeń myszy dla przycisku."""
    def handle_event(self, event, on_click_event):
        assert callable(on_click_event), "on_click_event musi być funkcją (callable)"

        # Kliknięcie lewym przyciskiem myszy na przycisk
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered():
            self.is_pressed = True

        # Ruch myszy poza przyciskiem resetuje stan kliknięcia
        elif event.type == pygame.MOUSEMOTION and not self.is_hovered():
            self.is_pressed = False

        # Zwolnienie lewego przycisku myszy
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered():
                on_click_event()  # Wywołanie funkcji przypisanej do kliknięcia
            self.is_pressed = False

    """Generuje widok presetu planszy, który można wyświetlić na przycisku dla
        dobrej przejrzystości jaki preset chce wybrać użytkownik do swojej gry."""

    @staticmethod
    def generate_preview_surface(board_layout, size):
        surface = pygame.Surface(size)
        surface.fill((220, 220, 220))

        rows = len(board_layout)
        cols = len(board_layout[0]) if rows > 0 else 0

        cell_width = size[0] / cols
        cell_height = size[1] / rows

        for y in range(rows):
            for x in range(cols):
                cell = board_layout[y][x]
                color = (10, 10, 10) if cell else (200, 200, 200)
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                pygame.draw.rect(surface, color, rect)

        return surface