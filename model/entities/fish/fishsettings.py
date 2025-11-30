from enum import Enum

from pygame import Vector2


class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2


class FishSettings:
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
