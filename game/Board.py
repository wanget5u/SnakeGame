import math
import random
import pygame

from core.Config import GAME_OVER
from core.Config import Config
from game.Block import Block
from game.CollisonEffect import CollisionEffect
from game.Effects import Effects
from game.Score import Score
from game.Snake import Snake
from game.Wall import Wall
from game.Fruits import Fruits
from game_engine.GameEngine import GameEngine
from game.Tile import Tile

"""Klasa zajmująca się wszelkimi wydarzeniami przebiegającymi podczas rozgrywki.
W zakres tej klasy wchodzi:
- inicjalizacja planszy do gry,
- inicjalizacja efektów pojawiających się na planszy,
- inicjalizacja bloków kolizyjnych pojawiających się podczas gry,
- inicjalizacja ciała węża oraz obsługa jego poruszania się

Klasa ta korzysta z metod z game_engine/GameEngine.py do obsługi wydarzeń.
"""
class Board:
    def __init__(self, size_x: int, size_y: int, board_preset: list[list[int]] = None):
        assert isinstance(size_x, int) and 10 <= size_x <= 25 and isinstance(size_y, int) and 10 <= size_y <= 25, "size_x oraz size_y muszą być dodatnimi liczbami całkowitymi w zakresie [10-25]"

        # Inicjalizacja podstawowych parametrów
        self.hud_height = int(Config.HUD_HEIGHT * Config.SCALE_Y) # Jaki dystans będzie plansza przesunięta na dół, aby labele Score oraz Time nie nachodziły na planszę
        self.size_x = size_x
        self.size_y = size_y
        self.step = None
        self.engine = self.create_engine() # Tworzenie instancji silnika

        # Inicjalizacja owoców
        self.fruit_spawn_time = Config.FRUIT_SPAWN_TIME
        self.fruits = pygame.sprite.Group()
        self.fruit_count = 0

        # Inicjalizacja bloków
        self.block_spawn_time = Config.BLOCK_SPAWN_TIME
        self.blocks = pygame.sprite.Group()
        self.block_count = 0

        # Inicjalizacja efektów
        self.effects_count = 0
        self.effects_spawn_time = Config.EFFECTS_SPAWN_TIME
        self.effects = pygame.sprite.Group()

        # Snake, ściany, kafelki
        self.snake = None
        self.walls = []
        self.tiles = []

        # Wynik i czas
        self.score = None
        self.time_elapsed = None

        # Inicjalizacja tablicy wyników i kafelków
        self.initialize_scoreboard()
        self.initialize_tiles()

        # Preset planszy będący słownikiem zawierającym pola:
        # index: int, difficulty: string, oraz layout: list[list[int, int]]
        self.board_preset = board_preset

        # print(board_preset["layout"])

        self.begin_time = pygame.time.get_ticks()

        self.init_effects = Effects()
        self.active_effects = []

    """Utworzenie silnika gry i wyznaczenie kroków siatki."""
    def create_engine(self):
        margin_ratio = 0.9

        max_board_pixel_size_x = int(Config.SCREEN_WIDTH * margin_ratio)
        max_board_pixel_size_y = int((Config.SCREEN_HEIGHT - self.hud_height) * margin_ratio)

        self.step = min(max_board_pixel_size_x // self.size_x, max_board_pixel_size_y // self.size_y)

        board_pixel_size_x = self.step * self.size_x
        board_pixel_size_y = self.step * self.size_y

        origin_x = (Config.SCREEN_WIDTH - board_pixel_size_x) // 2
        origin_y = self.hud_height + (Config.SCREEN_HEIGHT - self.hud_height - board_pixel_size_y) // 2

        return GameEngine(self.step, (origin_x, origin_y), (board_pixel_size_x, board_pixel_size_y))

    """Inicjalizacja liczników punktów oraz mierzenia czasu gry."""
    def initialize_scoreboard(self):
        hud_y = int(self.hud_height * 0.75)

        self.score = Score(int(Config.SCREEN_WIDTH * 0.75), hud_y, "Score", 140, int(220 * Config.SCALE_X))
        self.time_elapsed = Score(int(Config.SCREEN_WIDTH * 0.1), hud_y, "Time", 140, int(260 * Config.SCALE_X))

    """Mechanizm do losowego tworzenia obiektu na planszy. 
    Należy:
    - podać listę, do której zostanie dodany obiekt,
    - klasę obiektu dla walidacji,
    - ile 'ticków' zajmie pojawienie się obiektu na planszy,
    - obecna ilość 'ticków' jaka minęła,
    - nazwa obiektu dla debugowania w konsoli"""
    def spawn_object(self, group, cls, spawn_time, current_count, object_name="object"):
        if current_count >= spawn_time:
            max_attempts = 100
            attempt = 0

            while attempt < max_attempts:
                pos = self.generate_random_board_position()
                collides_with_snake = any(unit.rect.topleft == pos for unit in self.snake.body)
                collides_with_fruits = any(fruit.rect.topleft == pos for fruit in self.fruits)
                collides_with_blocks = any(block.rect.topleft == pos for block in self.blocks)
                collides_with_effects = any(effect.rect.topleft == pos for effect in self.effects)

                # Sprawdzanie czy nowy obiekt nie jest za blisko węża - byłoby
                # to niesprawiedliwe, aby obiekt miał się pojawić zaraz przed nim
                distance_from_snake = math.sqrt(
                    math.pow(pos[0] - self.snake.NEW_POS[0][0], 2) + math.pow(pos[1] - self.snake.NEW_POS[0][1], 2))

                # Upewnij się, że nowy obiekt nie koliduje z innymi obiektami
                if (    not collides_with_snake and
                        not collides_with_fruits and
                        not collides_with_blocks and
                        not collides_with_effects and
                        distance_from_snake > self.step * 3):
                    group.add(cls(pos, self.engine))
                    return 0
                attempt += 1 # Dodanie do licznika kolejnej próby pojawienia się obiektu na planszy
            else:
                print(f"Nie znaleziono miejsca na {object_name}")
                return current_count
        else:
            return current_count + 1

    """Tworzenie owocu na planszy."""
    def spawn_fruit(self):
        self.fruit_count = self.spawn_object(self.fruits, Fruits, 0, 0, "fruit")

    """Tworzenie bloku kolizyjnego na planszy."""
    def spawn_block(self):
        self.block_count = self.spawn_object(self.blocks, Block, self.block_spawn_time, self.block_count, "block")

    """Tworzenie efektu na planszy."""
    def spawn_effect(self):
        if len(self.effects) < 2:
            self.effects_count = self.spawn_object(self.effects, CollisionEffect, self.effects_spawn_time, self.effects_count, "effect")

    def load_preset(self):
        origin_x, origin_y = self.engine.board_offset_x, self.engine.board_offset_y
        layout = self.board_preset["layout"]
        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == 1:
                    block_x = (origin_x + (x * self.step)) * Config.SCALE_X
                    block_y = (origin_y + (y * self.step)) * Config.SCALE_Y
                    block_pos = pygame.math.Vector2(block_x, block_y)

                    self.blocks.add(Block(block_pos, self.engine))

    """Wygeneruj losową pozycję na planszy."""
    def generate_random_board_position(self):
        x = (random.randint(0, self.size_x - 1) * self.engine.step) + self.engine.board_offset_x
        y = (random.randint(0, self.size_y - 1) * self.engine.step) + self.engine.board_offset_y
        return pygame.math.Vector2(x, y)

    """Rysowanie całej planszy oraz jej komponentów."""
    def draw(self, screen):
        screen.fill(Config.WALL_COLOR) # Tło

        for wall in self.walls: wall.draw(screen)
        for tile in self.tiles: tile.draw(screen)

        self.fruits.draw(screen)
        self.blocks.draw(screen)
        self.effects.draw(screen)
        self.snake.render(screen)
        self.score.draw(screen)
        self.time_elapsed.draw(screen)

    """Inicjalizacja ścian planszy. 
    
    Note - początkowo miały to być ściany ograniczające planszę ale zmieniłem
    zdanie i zamiast męczyć się z 4-ma ścianami do poprawnego renderowania
    ustawiłem tło widoku gry na kolor ścian a samą ścianę, którą tutaj dodaję
    to tak naprawdę tło samej planszy. Lepiej tego nie tykać."""
    def initialize_walls(self):
        origin_x, origin_y = self.engine.board_offset_x, self.engine.board_offset_y
        board_size_x = self.engine.board_size_x
        board_size_y = self.engine.board_size_y
        self.walls.append(Wall(origin_x, origin_y, int(board_size_x // Config.SCALE_X), int(board_size_y // Config.SCALE_Y), Config.BOARD_COLOR))

    """Inicjalizacja poszczególnych pól na planszy."""
    def initialize_tiles(self):
        origin_x, origin_y = self.engine.board_offset_x, self.engine.board_offset_y
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.tiles.append(
                    Tile(origin_x + (x * self.step), origin_y + (y * self.step), (self.step - 3), Config.TILE_COLOR))

    """Inicjalizacja węża."""
    def initialize_snake(self):
        self.snake = Snake(self.engine)
        self.snake.set_start_pos()
        self.snake.initialize_body()

    """Aktualizacja aktywnych efektów oraz sprawdzanie czasu ich trwania."""
    def update_effects(self):
        for effect in self.active_effects:
            effect.effect.timer -= 1
            if effect.effect.timer <= 0:
                effect.revert()
                self.active_effects.remove(effect)

    """Aktualizacja wyświetlanego czasu gry."""
    def update_clock(self):
        elapsed_time_ms = pygame.time.get_ticks() - self.begin_time
        elapsed_time_sec = elapsed_time_ms // 1000
        minutes = elapsed_time_sec // 60
        seconds = elapsed_time_sec % 60
        formatted_time = f"{minutes:02}:{seconds:02}"
        self.time_elapsed.set_value(formatted_time)

    """Sprawdzenie czy wąż zjadł owoc."""
    def check_fruit_collision(self):
        for fruit in list(self.fruits):
            if self.engine.check_snake_collision_with_object(self.snake.body.sprites()[0].rect.topleft, fruit.rect.topleft):
                self.fruits.remove(fruit)
                self.snake.NEW_POS = self.engine.extend_snake(self.snake.NEW_POS)
                self.snake.PREV_POS = self.snake.NEW_POS.copy()
                self.snake.add_unit(self.snake.NEW_POS[-1])
                self.score.add(1)
                self.spawn_fruit()
                Config.SNAKE_SPEED *= 0.93

    """Sprawdzenie czy wąż zebrał efekt."""
    def check_effect_collision(self):
        for effect in self.effects:
            if self.engine.check_snake_collision_with_object(self.snake.body.sprites()[0].rect.topleft, effect.rect.topleft):
                effect.trigger()
                self.active_effects.append(effect)
                self.effects.remove(effect)

    """Sprawdzenie kolizji węża z samym sobą, ścianą lub z blokiem - koniec gry"""
    def check_snake_collision(self):
        for block in list(self.blocks):
            if self.engine.check_snake_collision_with_object(self.snake.body.sprites()[0].rect.topleft, block.rect.topleft):
                raise GAME_OVER("GAME OVER", self.score.value, self.time_elapsed.value)

        if self.engine.check_snake_collision(self.snake.NEW_POS):
            raise GAME_OVER("GAME OVER", self.score.value, self.time_elapsed.value)

    """Ustawienie nowego kierunku ruchu węża."""
    def set_snake_direction(self, direction):
        if not self.engine.is_proper_direction(self.snake.NEW_POS, direction):
            return
        self.snake.direction = direction

    """Aktualizacja logiki gry."""
    def update(self):
        self.update_clock()
        self.spawn_block()
        self.spawn_effect()
        self.update_effects()

    """Aktualizacja stanu gry w jednej klatce."""
    def update_tick(self):
        self.snake.update()
        self.check_fruit_collision()
        self.check_snake_collision()
        self.check_effect_collision()
