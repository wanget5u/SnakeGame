import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_move_snake_with_invalid_data(engine):
    with pytest.raises(AssertionError):
        engine.move_snake([(-1, -2), (1, 0)], Direction.UP)


def test_move_snake_with_empty_snake(engine):
    assert engine.move_snake([], Direction.UP) == []


def test_move_snake_collision_with_body(engine):
    with pytest.raises(AssertionError):
        engine.move_snake([(4, 4), (5, 4), (6, 4), (6, 3), (5, 3), (4, 3), (4, 4)], Direction.LEFT)


def test_move_snake_with_wrong_snake_body(engine):
    with pytest.raises(AssertionError):
        engine.move_snake([(2, 4), (3, 7)], Direction.RIGHT)
