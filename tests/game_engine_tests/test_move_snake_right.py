import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_move_snake_right_simple_move_without_collision(engine):
    assert engine.move_snake([(4, 7), (4, 6), (4, 5), (4, 4)], Direction.RIGHT) == [
        (5, 7), (4, 7), (4, 6), (4, 5)]


def test_move_snake_right_illegal_move(engine):
    with pytest.raises(AssertionError):
        assert engine.move_snake([(0, 0), (1, 0), (2, 0)], Direction.RIGHT)


def test_move_snake_right_collision_head_with_board_edge(engine):
    assert engine.move_snake([(9, 4), (8, 4), (7, 4), (6, 4)], Direction.RIGHT) == [
        (0, 4), (9, 4), (8, 4), (7, 4)]


def test_move_snake_right_collision_body_with_board_edge(engine):
    assert engine.move_snake([(0, 4), (9, 4), (8, 4), (7, 4)], Direction.RIGHT) == [
        (1, 4), (0, 4), (9, 4), (8, 4)]


def test_move_snake_right_with_one_unit_snake(engine):
    assert engine.move_snake([(9, 9)], Direction.RIGHT) == [(0, 9)]

def test_move_snake_right_with_step():
    engine = GameEngine(5, (0, 0), (20, 20))
    snake = engine.initialize_snake()
    new_snake = engine.move_snake(snake, Direction.RIGHT)
    assert new_snake[0] == (15, 10)
    assert len(new_snake) == 3

def test_move_snake_wrap_right():
    engine = GameEngine(5, (0, 0), (20, 20))
    snake = [(15, 10), (10, 10), (5, 10)]
    new_snake = engine.move_snake(snake, Direction.RIGHT)
    assert new_snake[0] == (0, 10)