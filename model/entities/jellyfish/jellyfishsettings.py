from enum import Enum

from pygame import Vector2


class JellyfishType(Enum):
    RED = 0


class JellyfishSettings:
    def __init__(
        self,
        jelly_type: JellyfishType,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        health: float,
        damage: float,
        start_position: Vector2 = Vector2(0.0, 0.0),
        start_velocity: Vector2 = Vector2(0.0, 0.0),
    ):
        self.jelly_type: JellyfishType = jelly_type
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.health: float = health
        self.damage: float = damage
        self.start_position: Vector2 = start_position
        self.start_velocity: Vector2 = start_velocity
