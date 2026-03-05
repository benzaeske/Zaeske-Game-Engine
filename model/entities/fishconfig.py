from model.entities.boidconfig import BoidConfig


class FishConfig:
    def __init__(self, max_speed: float, max_acceleration: float, boid_config: BoidConfig) -> None:
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.boid_config: BoidConfig = boid_config