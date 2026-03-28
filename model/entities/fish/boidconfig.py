from dataclasses import dataclass

from model.entities.physicsentityconfig import PhysicsEntityConfig


@dataclass
class BoidConfig(PhysicsEntityConfig):
    cohere_distance: float
    avoid_distance: float
    interaction_cell_range: int
    cohere_k: float
    avoid_k: float
    align_k: float