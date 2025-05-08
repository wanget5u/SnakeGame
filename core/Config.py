import os


class Config:
    # 16:9 1280x720
    BASE_WIDTH = 1280
    BASE_HEIGHT = 720
    SCALE_X = 1
    SCALE_Y = 1

    FULLSCREEN = False
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    GAME_TITLE = "Snake"
    GAME_DESCRIPTION = "By s31230 s31107 s31232 s31255"

    'Uniwersalne'
    TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = 60

    'MENU'
    MENU_COLOR = (33, 36, 37)
    MENU_BUTTON_COLOR = (130, 132, 133)

    'SETTINGS'
    SETTINGS_COLOR = (23, 26, 27)
    SETTINGS_BUTTON_COLOR = (110, 112, 113)
    SETTINGS_SLIDER_COLOR = (255, 255, 255)
    SETTINGS_RESOLUTION_SLIDER_POSITION = 0

    'GAME'
    FRUIT_SPAWN_TIME = 0
    DECELERATE_DURATION = 100
    ACCELERATE_DURATION = 100
    FRUIT_COLOR = (220, 50, 50)
    DECELERATE_COLOR = (205, 205, 35)
    ACCELERATE_COLOR = (35, 35, 180)
    NEUTRAL_COLOR = (255, 255, 255)
    HUD_HEIGHT = 80

    BLOCK_COLOR = (100, 100, 100)
    BLOCK_SPAWN_TIME = 25

    EFFECTS_SPAWN_TIME = 15

    ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

    'GAME CREATION'
    GAME_CREATION_GAME_SPEED_SLIDER_POSITION = 0

    'PAUSE MENU'
    MENU_PAUSE_COLOR = (23, 26, 27)

    'BOARD'
    BOARD_UPDATE_SPEED = 8
    BOARD_DIMENSIONS = (15, 15)
    BOARD_COLOR = (31, 33, 35)
    WALL_COLOR = (20, 22, 24)
    TILE_COLOR = (36, 38, 40)

    'SNAKE'
    SNAKE_SPEED = 10
    SNAKE_BASE_SPEED = SNAKE_SPEED
    BASE_UNIT_SIZE = 25
    UNIT_SIZE = 25
    UNIT_COLOR = (35, 140, 35)

    'DEFAULTS'
    SNAKE_SIZE = 3
    GAME_SPEED = 10

    'Służy do wyliczania skalowania komponentów oraz aktualizuje rozdzielczość na tą podaną w argumentach'
    @staticmethod
    def update_resolution(width, height):
        Config.SCREEN_WIDTH = width
        Config.SCREEN_HEIGHT = height
        Config.SCALE_X = width / Config.BASE_WIDTH
        Config.SCALE_Y = height / Config.BASE_HEIGHT

    @staticmethod
    def get_asset_path(filename):
        return os.path.join(Config.ASSETS_DIR, filename)

from enum import Enum

class WINDOW_STATE(Enum):
    MENU = 1
    SETTINGS = 2
    GAME = 3
    GAME_CREATION = 4
    MENU_PAUSE = 5
    LEADERBOARD = 6
    GAME_OVER = 7
    LOGIN = 8
    REGISTER = 9
    BOARD_SELECT = 10

class GAME_OVER(Exception):
    def __init__(self, message, score, time_elapsed):
        super().__init__(message)
        self.score = score
        self.time_elapsed = time_elapsed


import os
