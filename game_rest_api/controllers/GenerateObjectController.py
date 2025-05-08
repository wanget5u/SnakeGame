from http import HTTPStatus
from flask import Blueprint, jsonify
from game_rest_api import shared

generate_object_bp = Blueprint("generate_object", __name__)


# Przykład użycia: http://localhost:5000/generate_block
# Zwraca: wygenerowany blok
@generate_object_bp.route("/generate_block", methods=["POST"])
def generate_block():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    return jsonify({"generated_block": shared.board.generate_block()}), HTTPStatus.OK


# Przykład użycia: http://localhost:5000/generate_fruit
# Zwraca: wygenerowany owoc
@generate_object_bp.route("/generate_fruit", methods=["POST"])
def generate_fruit():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    return jsonify({"generated_fruit": shared.board.generate_fruit()}), HTTPStatus.OK