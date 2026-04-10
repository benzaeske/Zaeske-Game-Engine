from dataclasses import dataclass

from model.entities.configbase import ConfigBase
from view.sprite.spriteconfig import SpriteConfig


@dataclass
class PlayerConfig(ConfigBase):
    left_sprite: SpriteConfig
    right_sprite: SpriteConfig
    hitbox_width: float
    hitbox_height: float
    speed: float
    acceleration: float
    max_health: float

    @classmethod
    def from_dict(cls, data: dict) -> ConfigBase:
        data['left_sprite'] = SpriteConfig.from_dict(data['left_sprite'])
        data['right_sprite'] = SpriteConfig.from_dict(data['right_sprite'])
        return super().from_dict(data)