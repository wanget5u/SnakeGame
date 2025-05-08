from flask import jsonify, request, Blueprint

from game_rest_api.models.Board import Board
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from game_rest_api import shared
from http import HTTPStatus

init_bp = Blueprint("init", __name__)

initialize_params_schema = {
        "type": "object",
        "properties": {
            "step": {"type": "integer"},
            "board_offset": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 2,
                "maxItems": 2
            },
            "board_size": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 2,
                "maxItems": 2
            }
        },
        "required": ["step", "board_offset", "board_size"]
    }


class BoardInitializationInputs(Inputs):
    json = [JsonSchema(schema=initialize_params_schema)]


# Przykład użycia: http://localhost:5000/init
# Zwraca: ciało węża, wszystkie owoce i bloki na planszy
# Przykład parametrów(Wzorzec określony w zmiennej initialize_params_schema):
#    {
#        "step": 2,
#        "board_offset": [0, 0],
#        "board_size": [10, 10]
#    }
@init_bp.route('/init', methods=['POST'])
def initialize_board():
    board_inputs = BoardInitializationInputs(request)
    if not board_inputs.validate():
        return jsonify({"errors": board_inputs.errors}), HTTPStatus.BAD_REQUEST
    data = request.json
    try:
        shared.board = Board(data["step"], data["board_offset"], data["board_size"])
        # Przy inicjalizacji planszy generujemy owoc
        shared.board.generate_fruit()
    except Exception as error:
        return jsonify({"errors": str(error)}), HTTPStatus.BAD_REQUEST
    return jsonify({
        "snake_body": shared.board.snake, "fruits": shared.board.fruits, "blocks": shared.board.blocks}), HTTPStatus.OK
