import pygame

from core.Config import Config

class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, min_val: int, max_val: int, start_val: int):
        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(width, int) and width > 0, "width musi być dodatnią liczbą całkowitą"
        assert isinstance(height, int) and height > 0, "height musi być dodatnią liczbą całkowitą"
        assert isinstance(min_val, (int, float)), "min_val musi być liczbą"
        assert isinstance(max_val, (int, float)), "max_val musi być liczbą"
        assert isinstance(start_val, (int, float)), "start_val musi być liczbą"
        assert min_val < max_val, "min_val musi być mniejsze niż max_val"
        assert min_val <= start_val <= max_val, "start_val musi być w zakresie min_val i max_val"

        self.x = x
        self.y = y
        self.width = width * Config.SCALE_X
        self.height = height * Config.SCALE_Y
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val

        self.slider_size = self.height * 0.6

        self.min_slider_x = self.x + self.slider_size // 2 + 20
        self.max_slider_x = self.x + self.width - self.slider_size // 2 - 20

        self.slider_x = self.min_slider_x + ((start_val - self.min_val) / (self.max_val - self.min_val)) * (self.max_slider_x - self.min_slider_x)
        self.slider_y = self.y + self.height // 2

        self.dragging = False

    def draw(self, screen):
        assert isinstance(screen, pygame.Surface), "screen musi być instancją pygame.Surface"

        pygame.draw.rect(screen, Config.SETTINGS_BUTTON_COLOR,
                         (self.x, self.y, self.width, self.height),
                         border_radius=4)

        pygame.draw.rect(screen, tuple(min(255, int(x * 1.2)) for x in Config.SETTINGS_COLOR),
                         (self.x + self.slider_size // 2, self.y + self.slider_size // 2,
                          self.width - self.slider_size, self.height - self.slider_size),
                         border_radius=4)

        pygame.draw.rect(screen, Config.SETTINGS_SLIDER_COLOR,
                         (int(self.slider_x - self.slider_size // 2),
                          int(self.slider_y - self.slider_size // 2),
                          self.slider_size, self.slider_size),
                         border_radius=4)

    def is_hovered(self, mouse_position):
        assert isinstance(mouse_position, tuple) and len(mouse_position) == 2, "mouse_position musi być krotką (x, y)"
        return (self.slider_x - self.slider_size // 2 <= mouse_position[0] <= self.slider_x + self.slider_size // 2 and
                self.slider_y - self.slider_size // 2 <= mouse_position[1] <= self.slider_y + self.slider_size // 2)

    def handle_event(self, event):
        assert isinstance(event, pygame.event.EventType), "event musi być instancją pygame.event.EventType"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()

            self.slider_x = max(self.min_slider_x, min(mouse_x, self.max_slider_x))

            progress = (self.slider_x - self.min_slider_x) / (self.max_slider_x - self.min_slider_x)
            self.value = self.min_val + progress * (self.max_val - self.min_val)
