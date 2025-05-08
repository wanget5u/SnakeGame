from http import HTTPStatus
from flask import Blueprint, jsonify
from game_rest_api import shared

state_bp = Blueprint("state", __name__)


# Przykład użycia: http://localhost:5000/state
# Zwraca: ciało węża, wszystkie owoce i bloki na planszy
@state_bp.route('/state', methods=['GET'])
def get_state():
    if shared.board is None:
        return shared.non_initialize_board_strategy()
    return jsonify({
        "snake_body": shared.board.snake, "fruits": shared.board.fruits, "blocks": shared.board.blocks}), HTTPStatus.OK