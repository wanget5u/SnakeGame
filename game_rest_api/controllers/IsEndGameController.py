from http import HTTPStatus
from flask import Blueprint, jsonify
from game_rest_api import shared

is_end_game_bp = Blueprint("is_end_game", __name__)


# Przykład użycia: http://localhost:5000/is_end_game
# Zwraca: true/false
@is_end_game_bp.route('/is_end_game', methods=['GET'])
def is_end_game():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    return jsonify({"is_end_game": shared.board.is_end_game()}), HTTPStatus.OK