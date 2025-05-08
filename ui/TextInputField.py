import pygame

from core.Config import Config
from ui.Button import Button

class TextInputField:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple[int, int, int], text_color: tuple[int, int, int], is_password: bool = False, max_length: int = 18):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(text, str), "text musi być typu str"
        assert isinstance(color, tuple) and len(color) == 3 and all(0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(text_color, tuple) and len(text_color) == 3 and all( 0 <= c <= 255 for c in text_color), "text_color musi być krotką 3 liczb całkowitych z zakresu 0-255"
        assert isinstance(max_length, int) and max_length > 0, "max_length musi być dodatnią liczbą całkowitą"
        assert isinstance(is_password, bool), "is_password musi być typu bool"

        self.width = width * Config.SCALE_X
        self.height = height * Config.SCALE_Y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.rect.center = (x * Config.SCALE_X, y * Config.SCALE_Y)

        self.color_inactive = color
        self.color_active = tuple(min(255, int(c * 1.5)) for c in color)
        self.font = pygame.font.SysFont(None, int(60 * Config.SCALE_Y))
        self.color = self.color_inactive
        self.active = False
        self.text = text
        self.max_length = max_length
        self.is_password = is_password
        self.password_visible = False
        self.text_color = text_color

        self.toggle_button = None

        if self.is_password:
            button_width = int(width * 0.3 * Config.SCALE_X)
            button_height = int(height * 0.9 * Config.SCALE_Y)

            button_x = int(self.rect.right - button_width // 2)
            button_y = int(self.rect.centery)

            self.toggle_button = Button(
                int(button_x // Config.SCALE_X + 165), int(button_y // Config.SCALE_Y),
                int(button_width // Config.SCALE_X), int(button_height // Config.SCALE_Y), "show",
                Config.SETTINGS_BUTTON_COLOR,
                Config.TEXT_COLOR)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        if self.toggle_button:
            self.toggle_button.handle_event(event, self.toggle_password_visibility)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_DELETE:
                self.text = ""
            elif len(self.text) < self.max_length and event.unicode.isalnum():
                self.text += event.unicode

    def toggle_password_visibility(self):
        self.password_visible = not self.password_visible
        self.toggle_button.text = "hide" if self.password_visible else "show"

    def draw(self, surface):
        display_text = self.text if (not self.is_password or self.password_visible) else '*' * len(self.text)

        txt_surface = self.font.render(display_text, True, self.text_color)
        text_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, text_rect)
        pygame.draw.rect(surface, self.color, self.rect, 5)

        if self.toggle_button:
            self.toggle_button.draw(surface)
