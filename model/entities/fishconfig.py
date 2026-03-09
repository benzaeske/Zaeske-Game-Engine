from enum import Enum

from model.entities.boidconfig import BoidConfig

class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2

class FishConfig:
    def __init__(
            self,
            fish_type: FishType,
            sprite_w: float,
            sprite_h: float,
            max_speed: float,
            max_acceleration: float,
            boid_config: BoidConfig
    ) -> None:
        self.fish_type: FishType = fish_type
        self.sprite_w: float = sprite_w
        self.sprite_h: float = sprite_h
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.boid_config: BoidConfig = boid_config