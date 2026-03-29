from dataclasses import dataclass
from typing import Optional

from model.entities.physicsentityconfig import PhysicsEntityConfig
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from view.sprite.spriteconfig import SpriteConfig


@dataclass
class EnemyConfig(PhysicsEntityConfig, SpriteConfig):
    hitbox_width: float
    hitbox_height: float
    hp: float
    damage: float
    neighbor_cell_range: int
    avoid_neighbor_dist: float
    avoid_neighbor_k: float
    # Optional parameters to opt into fear behavior.
    # Enemies with this defined will run away from entities associated with the provided entity index
    is_afraid: bool = False
    afraid_of_index: Optional[EntityManagerIndex] = None
    scared_cell_range: Optional[int] = None
    scared_dist: Optional[float] = None
    scared_k: Optional[int] = None

