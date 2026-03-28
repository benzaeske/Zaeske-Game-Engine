from dataclasses import dataclass
from typing import Optional

from model.entities.entitytype import EntityType
from model.entities.physicsentityconfig import PhysicsEntityConfig
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
    # Enemies with this defined will run away from the provided entity type
    is_afraid: bool = False
    afraid_of_type: Optional[EntityType] = None
    scared_cell_range: Optional[int] = None
    scared_dist: Optional[float] = None
    scared_k: Optional[int] = None

