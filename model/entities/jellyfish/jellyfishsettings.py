from enum import Enum


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
        neighbor_range: int,
        scared_range: int,
    ):
        self.jelly_type: JellyfishType = jelly_type
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.health: float = health
        self.damage: float = damage
        self.neighbor_range: int = neighbor_range
        self.scared_range: int = scared_range
