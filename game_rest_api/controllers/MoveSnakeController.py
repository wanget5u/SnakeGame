from http import HTTPStatus
from flask import Blueprint, request, jsonify
from game_engine.GameEngine import Direction
from game_rest_api import shared

snake_movement_bp = Blueprint("snake_movement", __name__)


# Przykład użycia: http://localhost:5000/snake_move?direction=UP
# Zwraca: ciało węża po wykonaniu ruchu
@snake_movement_bp.route("/snake_move", methods=["PUT"])
def snake_move():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    try:
        shared.board.move_snake(Direction[request.args.get("direction")])
        return jsonify({"snake_body": shared.board.snake}), HTTPStatus.OK
    except ValueError:
        return jsonify({"errors": "Wrong direction"}), HTTPStatus.BAD_REQUEST
    except Exception as error:
        return jsonify({"errors": str(error)}), HTTPStatus.BAD_REQUEST