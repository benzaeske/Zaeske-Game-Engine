from dataclasses import dataclass

from model.entities.fish.boidconfig import BoidConfig
from view.sprite.spriteconfig import SpriteConfig


@dataclass
class FishConfig(BoidConfig, SpriteConfig):
    shoal: bool
    shoal_radius: float
    shoal_k: float
