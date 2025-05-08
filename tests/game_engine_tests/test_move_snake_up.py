import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_move_snake_up_simple_move_without_collision(engine):
    assert engine.move_snake([(0, 0), (1, 0), (2, 0)], Direction.UP) == [(0, 1), (0, 0), (1, 0)]


def test_move_snake_up_illegal_move(engine):
    with pytest.raises(AssertionError):
        assert engine.move_snake([(4, 4), (4, 5), (4, 6), (4, 7)], Direction.UP)


def test_move_snake_up_collision_head_with_board_edge(engine):
    assert engine.move_snake([(4, 9), (4, 8), (4, 7), (4, 6)], Direction.UP) == [
        (4, 0), (4, 9), (4, 8), (4, 7)]


def test_move_snake_up_collision_body_with_board_edge(engine):
    assert engine.move_snake([(4, 0), (4, 9), (4, 8), (4, 7)], Direction.UP) == [
        (4, 1), (4, 0), (4, 9), (4, 8)]


def test_move_snake_up_with_one_unit_snake(engine):
    assert engine.move_snake([(9, 9)], Direction.UP) == [(9, 0)]
