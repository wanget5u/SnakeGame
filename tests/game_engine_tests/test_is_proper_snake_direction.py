import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0, ), (10, 10, ))


def test_not_proper_snake_direction(engine):
    assert not engine.is_proper_direction([(2, 7), (2, 6), (2, 5), (2, 4)], Direction.DOWN)


def test_not_proper_direction_through_wall(engine):
    assert not engine.is_proper_direction([(2, 9), (2, 0), (2, 1), (2, 2)], Direction.UP)


def test_proper_direction_test(engine):
    assert engine.is_proper_direction([(1, 3), (1, 2), (1, 1)], Direction.UP)


def test_snake_wrong_snake_body(engine):
    with pytest.raises(AssertionError):
        engine.check_snake_collision([(6, 3), (3, 5)])