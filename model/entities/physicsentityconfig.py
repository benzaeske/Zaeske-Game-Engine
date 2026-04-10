from dataclasses import dataclass

from model.entities.entityconfig import EntityConfig

@dataclass
class PhysicsEntityConfig(EntityConfig):
    max_speed: float
    max_acceleration: float