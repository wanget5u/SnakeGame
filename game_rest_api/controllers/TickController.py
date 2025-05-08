from flask import Blueprint, request, jsonify
from http import HTTPStatus
from game_rest_api import shared
from game_engine.GameEngine import Direction

tick_bp = Blueprint("tick", __name__)

# Zamiast wielu kontrolerów używamy jednego, który robi kilka rzeczy. Jedyne co trzeba zrobić to wywołać go co jakiś czas.

@tick_bp.route('/tick', methods=['PUT'])
def tick():
    if shared.board is None:
        return shared.non_initialize_board_strategy()

    # Najpierw parsujemy kierunek
    dir_str = request.args.get("direction", "")
    try:
        direction = Direction[dir_str]
    except KeyError:
        return jsonify({"errors": "Wrong direction"}), HTTPStatus.BAD_REQUEST

    # Potem wykonujemy ruch, i to TU łapiemy wyjście węża za mapę
    try:
        shared.board.move_snake(direction)
    except AssertionError:
        # silnik rzucił błędem bo wąż wyszedł poza mapę
        return jsonify({
            "snake":       shared.board.snake,
            "fruits":      shared.board.fruits,
            "blocks":      shared.board.blocks,
            "is_end_game": True
        }), HTTPStatus.OK

    # Jak nie ma owoca to jeden generujemy
    if not shared.board.fruits:
        shared.board.generate_fruit()

    # Sprawdzamy kolizję z samym sobą czy z przeszkodą
    try:
        end = shared.board.is_end_game()
    except AssertionError:
        # jeśli z jakiegoś powodu silnik nadal rzuca asercję spójności traktujemy to jako game over
        end = True

    # Zwracamy stan gry
    return jsonify({
        "snake":       shared.board.snake,
        "fruits":      shared.board.fruits,
        "blocks":      shared.board.blocks,
        "is_end_game": end
    }), HTTPStatus.OK
