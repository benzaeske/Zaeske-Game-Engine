from enum import Enum

from model.entities.fish.boidconfigv1 import BoidConfigV1

class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2

class FishConfigV1:
    def __init__(
            self,
            fish_type: FishType,
            max_speed: float,
            max_acceleration: float,
            boid_config: BoidConfigV1,
            shoal: bool,
            shoal_radius: float | None = None,
            shoal_k: float | None = None,
    ) -> None:
        self.fish_type: FishType = fish_type
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.boid_config: BoidConfigV1 = boid_config
        self.shoal: bool = shoal
        if shoal:
            if shoal_radius is None:
                raise ValueError("shoal_radius must be defined when shoal is True")
            if shoal_k is None:
                raise ValueError("shoal_k must be defined when shoal is True")
        self.shoal_radius: float | None = shoal_radius
        self.shoal_k: float | None = shoal_k