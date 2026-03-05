from enum import Enum

from model.entities.boidconfig import BoidConfig

class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2

class FishConfig:
    def __init__(self, type: FishType, max_speed: float, max_acceleration: float, boid_config: BoidConfig) -> None:
        self.type = type
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.boid_config: BoidConfig = boid_config