from dataclasses import dataclass

from model.entities.items.projectileconfig import ProjectileConfig


@dataclass
class ShieldConfig(ProjectileConfig):
    radius: float