from dataclasses import dataclass

from model.entities.entityconfig import EntityConfig


@dataclass
class SpriteConfig(EntityConfig):
    sprite_width: int
    sprite_height: int
    # TODO define sprite animation data