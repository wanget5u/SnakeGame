from http import HTTPStatus
from flask import Blueprint, request, jsonify
from game_engine.GameEngine import Direction
from game_rest_api import shared

is_proper_direction_bp = Blueprint("is_proper_direction", __name__)


# Przykład użycia: http://localhost:5000/is_proper_direction?direction=DOWN
# Zwraca: true/false
@is_proper_direction_bp.route("/is_proper_direction", methods=["GET"])
def is_proper_direction():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    try:
        return jsonify({"is_proper_direction": shared.board.is_proper_direction(
            Direction[request.args.get("direction")])}), HTTPStatus.OK
    except ValueError:
        return jsonify({"errors": "Wrong direction"}), HTTPStatus.BAD_REQUEST