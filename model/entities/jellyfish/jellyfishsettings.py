from enum import Enum

from pygame import Vector2


class JellyFishType(Enum):
    RED = 0


class JellyfishSettings:
    def __init__(
        self,
        jelly_type: JellyFishType,
        width: float,
        height: float,
        start_position: Vector2,
        start_velocity: Vector2,
        max_speed: float,
        max_acceleration: float,
        health: float,
        damage: float,
    ):
        self.jelly_type: JellyFishType = jelly_type
        self.width: float = width
        self.height: float = height
        self.start_position: Vector2 = start_position
        self.start_velocity: Vector2 = start_velocity
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.health: float = health
        self.damage: float = damage
