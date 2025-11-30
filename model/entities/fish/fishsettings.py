from enum import Enum

from pygame import Vector2


class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2


class FishSettings:
    """
    Defines properties for an individual Fish entity
    :param fish_type: The type of fish to use. This determines which fish sprite gets loaded from the images directory
    :param width: The width of the fish in the model. The fish sprite will be initially scaled to this size
    :param height: The height of the fish in the model. The fish sprite will be initially scaled to this size
    :param max_speed: The maximum allowed magnitude of this Fish's velocity
    :param max_acceleration: The maximum magnitude of this Fish's acceleration per frame
    :param initial_position: The initial position of the Fish
    :param initial_velocity: The initial velocity of the Fish
    """

    def __init__(
        self,
        fish_type: FishType,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        initial_position: Vector2 = Vector2(0.0, 0.0),
        initial_velocity: Vector2 = Vector2(0.0, 0.0),
    ) -> None:
        self.fish_type: FishType = fish_type
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.initial_position: Vector2 = initial_position
        self.initial_velocity: Vector2 = initial_velocity
