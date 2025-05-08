import pytest

from game_engine.GameEngine import GameEngine


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_snake_no_collision(engine):
    assert not engine.check_snake_collision([(5, 6), (5, 7), (5, 8), (4, 8)])


def test_snake_no_collision_board_collision(engine):
    assert not engine.check_snake_collision([(4, 0), (4, 9), (4, 8), (4, 7)])


def test_snake_collision(engine):
    assert engine.check_snake_collision(
        [(5, 7), (5, 6), (5, 5), (5, 4), (6, 4), (6, 5), (6, 6), (6, 7), (5, 7), (4, 7), (3, 7)])


def test_snake_wrong_snake_body(engine):
    with pytest.raises(AssertionError):
        engine.check_snake_collision([(2, 3), (5, 5)])


def test_snake_collision_long_body(engine):
    assert engine.check_snake_collision(
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (0, 0)])
