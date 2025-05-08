import random
from game_engine import GameEngine
from game_engine.GameEngine import Direction


class Board:
    def __init__(self, step: int, board_offset: tuple[int, int], board_size: tuple[int, int]):
        self.engine = GameEngine(step, board_offset, board_size)
        self.snake = self.engine.initialize_snake()
        self.fruits = []
        self.blocks = []

    def move_snake(self, direction: Direction) -> None:
        self.snake = self.engine.move_snake(self.snake, direction)
        if self.engine.check_snake_collision_with_objects(self.snake[0], self.fruits):
            self.fruits.remove(self.snake[0])
            self.snake = self.engine.extend_snake(self.snake)

    def is_end_game(self) -> bool:
        try:
            if self.engine.check_snake_collision(self.snake):
                return True
            if self.engine.check_snake_collision_with_objects(self.snake[0], self.blocks):
                return True
            return False
        except AssertionError:
            return True

    def is_proper_direction(self, direction: Direction) -> bool:
        return self.engine.is_proper_direction(self.snake, direction)

    def generate_block(self) -> tuple[int, int]:
        return self._generate_object_avoiding(self.blocks, append_to=self.blocks)

    def generate_fruit(self) -> tuple[int, int]:
        return self._generate_object_avoiding(self.fruits, append_to=self.fruits)


    # Losowanie nowej pozycji na planszy, bez kolizji z wężem ani z niczym innym
    def _generate_object_avoiding(
            self,
            target_list: list[tuple[int, int]],
            append_to: list[tuple[int, int]]
    ) -> tuple[int, int] | None:
        step = self.engine.step
        ox, oy = self.engine.board_offset_x, self.engine.board_offset_y
        sx, sy = self.engine.board_size_x, self.engine.board_size_y
        cols = sx // step
        rows = sy // step

        max_attempts = 100
        for _ in range(max_attempts):
            cx = random.randrange(cols)
            cy = random.randrange(rows)
            pos = (ox + cx * step, oy + cy * step)
            # unikanie węża i istniejących obiektów
            if pos in self.snake:      continue
            if pos in self.blocks:     continue
            if pos in target_list:     continue
            append_to.append(pos)
            return pos
        return None