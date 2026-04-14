from dataclasses import dataclass

from model.entities.entityconfig import EntityConfig

@dataclass
class ShieldConfig(EntityConfig):
    radius: float
    cooldown: float
    damage: float
    knockback_force: float