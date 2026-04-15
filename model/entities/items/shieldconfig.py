from dataclasses import dataclass

from model.entities.items.projectileconfig import ProjectileConfig
from view.sprite.spriteconfig import SpriteConfig


@dataclass
class ShieldConfig(ProjectileConfig, SpriteConfig):
    radius: float