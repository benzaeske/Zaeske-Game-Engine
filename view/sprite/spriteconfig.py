from dataclasses import dataclass

from model.entities.configbase import ConfigBase


@dataclass
class SpriteConfig(ConfigBase):
    sprite_width: int
    sprite_height: int
    image_location: str