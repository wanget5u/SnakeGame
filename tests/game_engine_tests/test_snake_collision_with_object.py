import pytest

from game_engine.GameEngine import GameEngine, Direction

@pytest.fixture
def engine():
    return GameEngine(1, (0, 0), (10, 10))

def test_check_snake_collision_with_object_normal(engine):
    #przypadek 1 - kolizja
    snake_head = (5, 5)
    object_coordinates = (5, 5)
    result = engine.check_snake_collision_with_object(snake_head, object_coordinates)
    assert result is True

    #przypadek 2 - brak kolizji
    snake_head = (5, 5)
    object_coordinates = (5, 6)
    result = engine.check_snake_collision_with_object(snake_head, object_coordinates)
    assert result is False


def test_check_snake_collision_with_object_wrong(engine):
    # zła długość tuple
    with pytest.raises(AssertionError):
        engine.check_snake_collision_with_object((5,), (5, 5))

    # koordynaty poza planszą
    with pytest.raises(AssertionError):
        engine.check_snake_collision_with_object((5, 5), (10, 5))