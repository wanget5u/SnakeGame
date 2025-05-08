from abc import ABC, abstractmethod



class EffectsManager(ABC):
    POSITIVE_EFFECTS = []
    NEGATIVE_EFFECTS = []
    NEUTRAL_EFFECT = []
    ALL_EFFECTS = [POSITIVE_EFFECTS, NEGATIVE_EFFECTS, NEUTRAL_EFFECT]

    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def revert(self): pass

    def __init__(self):
        self.color = (255, 255, 255)
        self.name = "UnnamedEffect"
        self.duration = 300
        self.timer = self.duration
        self.image_path = None
        self.previous_speed = None

    @classmethod
    def register_effect(cls, *, positive=True, neutral=False, name="Unknown", color=(255, 255, 255), duration=300, image_path, previous_speed, execute_fn=None, revert_fn=None):
        if not (callable(execute_fn) and callable(revert_fn)):
            raise ValueError("Musisz podać execute_fn i revert_fn")

        def __init__(self):
            super(dynamic_cls, self).__init__()
            self.name = name
            self.color = color
            self.duration = duration
            self.timer = duration
            self.image_path = image_path
            self.previous_speed = previous_speed

        dynamic_cls = type(name, (cls,), {
            "__init__": __init__,
            "execute": execute_fn,
            "revert": revert_fn
        })

        instance = dynamic_cls()

        if neutral:
            cls.NEUTRAL_EFFECT.append(instance)
        elif positive:
            cls.POSITIVE_EFFECTS.append(instance)
        else:
            cls.NEGATIVE_EFFECTS.append(instance)
