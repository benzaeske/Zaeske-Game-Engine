import pygame
from pygame import Surface, Vector2

from model.entities.jellyfish.jellyfish import Jellyfish
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyfishType


class JellyfishSpawner:
    def __init__(self, jellyfish_settings: JellyfishSettings, amount: int):
        self.jellyfish_settings: JellyfishSettings = jellyfish_settings
        self.sprite = self.get_jelly_sprite(
            jellyfish_settings.jelly_type,
            jellyfish_settings.width,
            jellyfish_settings.height,
        )
        self.amount: int = amount

    @staticmethod
    def get_jelly_sprite(
        jelly_type: JellyfishType, width: float, height: float
    ) -> Surface:
        match jelly_type:
            case JellyfishType.RED:
                surface: Surface = pygame.image.load(
                    "images/red_jellyfish.png"
                ).convert_alpha()
                return pygame.transform.scale(surface, (width, height))

    def spawn_jellyfish(
        self,
        player_pos: Vector2,
        camera_w: float,
        camera_h: float,
        world_w: float,
        world_h: float,
    ) -> Jellyfish:
        """Create a new jellyfish at a random position outside camera range but within the world boundary"""
        pass
