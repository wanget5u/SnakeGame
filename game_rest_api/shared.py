from http import HTTPStatus
from flask import jsonify

board = None

def non_initialize_board_strategy():
    return jsonify({"errors": "Board not initialized"}), HTTPStatus.NOT_FOUND