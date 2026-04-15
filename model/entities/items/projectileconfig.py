from dataclasses import dataclass

from model.entities.entityconfig import EntityConfig


@dataclass
class ProjectileConfig(EntityConfig):
    damage: float
    knockback_force: float
    cooldown: float
    cell_range: int