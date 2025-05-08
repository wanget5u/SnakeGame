from flask import Flask, send_from_directory
from flask_cors import CORS
from game_rest_api.controllers import BoardInitializationController, BoardStateController, GenerateObjectController, \
    IsEndGameController, IsProperDirectionController, MoveSnakeController, TickController


app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

for blueprint in (
        BoardInitializationController.init_bp, BoardStateController.state_bp,
        GenerateObjectController.generate_object_bp, IsEndGameController.is_end_game_bp,
        IsProperDirectionController.is_proper_direction_bp, MoveSnakeController.snake_movement_bp,TickController.tick_bp, ):
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def fallback(error):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()