import pytest

from game_engine.GameEngine import GameEngine, Direction


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_move_snake_left_simple_move_without_collision(engine):
    assert engine.move_snake([(4, 7), (4, 6), (4, 5), (4, 4)], Direction.LEFT) == [
        (3, 7), (4, 7), (4, 6), (4, 5)]


def test_move_snake_left_illegal_move(engine):
    with pytest.raises(AssertionError):
        assert engine.move_snake([(2, 0), (1, 0), (0, 0)], Direction.LEFT)


def test_move_snake_left_collision_head_with_board_edge(engine):
    assert engine.move_snake([(0, 4), (1, 4), (2, 4), (3, 4)], Direction.LEFT) == [
        (9, 4), (0, 4), (1, 4), (2, 4)]


def test_move_snake_left_collision_body_with_board_edge(engine):
    assert engine.move_snake([(9, 4), (0, 4), (1, 4), (2, 4)], Direction.LEFT) == [
        (8, 4), (9, 4), (0, 4), (1, 4)]


def test_move_snake_left_with_one_unit_snake(engine):
    assert engine.move_snake([(0, 9)], Direction.LEFT) == [(9, 9)]

def test_move_snake_left_with_step():
    engine = GameEngine(5, (0, 0), (20, 20))
    snake = [(10, 15), (10, 10), (10, 5)]
    new_snake = engine.move_snake(snake, Direction.LEFT)
    assert new_snake[0] == (5, 15)
    assert len(new_snake) == 3