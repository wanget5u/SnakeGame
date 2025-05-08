import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0, ), (10, 10, ))


def test_move_snake_down_simple_move_without_collision(engine):
    assert engine.move_snake([(2, 1), (1, 1), (0, 1)], Direction.DOWN) == [(2, 0), (2, 1), (1, 1)]


def test_move_snake_down_illegal_move(engine):
    with pytest.raises(AssertionError):
        engine.move_snake([(3, 7), (3, 6), (3, 5), (3, 4)], Direction.DOWN)


def test_move_snake_down_collision_head_with_board_edge(engine):
    assert engine.move_snake([(3, 0), (3, 1), (3, 2), (3, 3)], Direction.DOWN) == [
        (3, 9), (3, 0), (3, 1), (3, 2)]


def test_move_snake_down_collision_body_with_board_edge(engine):
    assert engine.move_snake([(3, 9), (3, 0), (3, 1), (3, 2)], Direction.DOWN) == [
        (3, 8), (3, 9), (3, 0), (3, 1)]


def test_move_snake_down_with_one_unit_snake(engine):
    assert engine.move_snake([(0, 0)], Direction.DOWN) == [(0, 9)]
