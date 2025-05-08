import pytest

from game_engine.GameEngine import GameEngine


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_is_within_bounds_collision_right_bound(engine):
    assert engine.is_within_bounds((10, 0))


def test_is_within_bounds_collision_left_bound(engine):
    assert engine.is_within_bounds((-1, 0))


def test_is_within_bounds_collision_top_bound(engine):
    assert engine.is_within_bounds((0, 10))


def test_is_within_bounds_collision_down_bound(engine):
    assert engine.is_within_bounds((0, -1))


def test_is_within_bounds_no_collision(engine):
    assert not engine.is_within_bounds((0, 0))


def test_is_within_bounds_wrong_data(engine):
    with pytest.raises(AssertionError):
        engine.is_within_bounds((1.5, 2.3))
