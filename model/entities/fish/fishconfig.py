from enum import Enum

from model.entities.fish.boidconfig import BoidConfig

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
            boid_config: BoidConfig,
            hatch_radius: float,
            shoal: bool,
            shoal_radius: float | None = None,
            shoal_k: float | None = None,
    ) -> None:
        self.fish_type: FishType = fish_type
        self.sprite_w: float = sprite_w
        self.sprite_h: float = sprite_h
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.boid_config: BoidConfig = boid_config
        self.hatch_radius: float = hatch_radius
        self.shoal: bool = shoal
        if shoal:
            if shoal_radius is None:
                raise ValueError("shoal_radius must be defined when shoal is True")
            if shoal_k is None:
                raise ValueError("shoal_k must be defined when shoal is True")
        self.shoal_radius: float | None = shoal_radius
        self.shoal_k: float | None = shoal_k