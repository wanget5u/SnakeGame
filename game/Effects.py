from core import Config
from game.EffectsManager import EffectsManager

class Effects:
    def __init__(self):
        Effects.init_positive_effects()
        Effects.init_negative_effects()
        Effects.init_neutral_effect()

    @staticmethod
    def init_positive_effects():
        EffectsManager.register_effect(
            positive=True,
            name="SpeedDecrease",
            color=Config.DECELERATE_COLOR,
            duration=Config.DECELERATE_DURATION,
            image_path=Config.get_asset_path('slow_down.png'),
            previous_speed=Config.SNAKE_SPEED,
            execute_fn=lambda self: setattr(Config, "SNAKE_SPEED", Config.SNAKE_SPEED * 1.2),
            revert_fn=lambda self: setattr(Config, "SNAKE_SPEED", self.previous_speed)
        )

    @staticmethod
    def init_negative_effects():
        EffectsManager.register_effect(
            positive=False,
            name="SpeedIncrease",
            color=Config.ACCELERATE_COLOR,
            duration=Config.ACCELERATE_DURATION,
            image_path=Config.get_asset_path('speed_boost.png'),
            previous_speed=Config.SNAKE_SPEED,
            execute_fn=lambda self: setattr(Config, "SNAKE_SPEED", Config.SNAKE_SPEED * 0.8),
            revert_fn=lambda self: setattr(Config, "SNAKE_SPEED", self.previous_speed)
        )

    @staticmethod
    def init_neutral_effect():
        EffectsManager.register_effect(
            neutral=True,
            name="Neutral",
            color=Config.NEUTRAL_COLOR,
            image_path=Config.get_asset_path('neutral_effect.png'),
            previous_speed=Config.SNAKE_SPEED,
            execute_fn=lambda self: None,
            revert_fn=lambda self: None
        )