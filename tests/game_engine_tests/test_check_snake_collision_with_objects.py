import pytest

from game_engine.GameEngine import GameEngine


@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))


def test_check_snake_collision_with_objects_normal(engine):
    # przypadek 1 - kolizja
    snake_head = (5, 5)
    objects_coordinates = [(9, 5), (5, 5)]
    result = engine.check_snake_collision_with_objects(snake_head, objects_coordinates)
    assert result is True

    # przypadek 2 - brak kolizji
    snake_head = (5, 5)
    objects_coordinates = [(9, 5), (6, 6)]  # (9,5), (6,6) does not match snake_head.
    result = engine.check_snake_collision_with_objects(snake_head, objects_coordinates)
    assert result is False


def test_check_snake_collision_with_objects_wrong(engine):
    # niepoprawna struktura głowy
    with pytest.raises(AssertionError):
        engine.check_snake_collision_with_objects((5,), [(9, 5), (5, 5)])

    # obiekty poza planszą
    with pytest.raises(AssertionError):
        engine.check_snake_collision_with_objects((5, 5), [(5, 5), (10, 6)])

    # koordynaty nie są listą tupli
    with pytest.raises(AssertionError):
        engine.check_snake_collision_with_objects((5, 5), "not a list")
