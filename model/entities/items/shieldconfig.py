from dataclasses import dataclass

from model.entities.entityconfig import EntityConfig

@dataclass
class ShieldConfig(EntityConfig):
    radius: float
    damage: float
    max_charge: int
    charge_delay: float