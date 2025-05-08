import pytest

from game_engine.GameEngine import GameEngine

def test_extend_snake():
    engine = GameEngine(5, (0,0), (20, 20))
    snake = engine.initialize_snake()
    extend_point = (15, 10)
    new_snake = engine.extend_snake(snake.copy())
    assert new_snake[-1] == extend_point
    assert len(new_snake) == len(snake) + 1

def test_extend_snake_with_collision():
    engine = GameEngine(5, (0,0), (10, 10))
    snake = [(10, 10), (5,10), (10, 10)]
    with pytest.raises(AssertionError):
        engine.extend_snake(snake.copy())