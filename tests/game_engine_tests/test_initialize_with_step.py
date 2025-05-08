import pytest

from game_engine.GameEngine import GameEngine


def test_valid_initialization():
    engine = GameEngine(5, (0, 0), (20, 20))
    assert engine.step == 5
    assert engine.board_size_x == 20
    assert engine.board_size_y == 20

def test_invalid_step_not_dividing_board():
    with pytest.raises(AssertionError):
        GameEngine(3, (0,0), (20,20))

def test_invalid_step_too_high():
    with pytest.raises(AssertionError):
        GameEngine(20, (0,0) , (20, 20))

def test_initialize_snake():
    engine = GameEngine(5, (0, 0), (20, 20))
    snake = engine.initialize_snake()
    expected = [(10, 10) , (5, 10) , (0, 10)]
    assert snake == expected

def test_initialize_with_different_offset():
    engine = GameEngine(3, (1, 1), (12, 15))
    snake = engine.initialize_snake()
    expected = [(7, 7) , (4, 7) , (1, 7)]
    assert snake == expected