import random

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
                    "images/red_jelly.png"
                ).convert_alpha()
                return pygame.transform.scale(surface, (width, height))

    def spawn_jellyfish(
        self,
        player_pos: Vector2,
        camera_w_adj: float,
        camera_h_adj: float,
        world_w: float,
        world_h: float,
    ) -> Jellyfish:
        """Create a new jellyfish at a random position outside camera range but within the world boundary"""
        # Pick between 2 different ranges: one between 0 and the camera edge, the other between the camera edge and the far world boundary
        x_ranges = [
            [0, player_pos.x - camera_w_adj],
            [player_pos.x + camera_w_adj, world_w]
        ]
        x_weights = [interval[1] - interval[0] for interval in x_ranges]
        x_range = random.choices(x_ranges, weights=x_weights, k=1)[0]
        x_pos = random.uniform(x_range[0], x_range[1])

        y_ranges = [
            [0, player_pos.y - camera_h_adj],
            [player_pos.y + camera_h_adj, world_h]
        ]
        y_weights = [interval[1] - interval[0] for interval in y_ranges]
        y_range = random.choices(y_ranges, weights=y_weights, k=1)[0]
        y_pos = random.uniform(y_range[0], y_range[1])

        return Jellyfish(self.sprite,
                         JellyfishSettings(
                             self.jellyfish_settings.jelly_type,
                             self.jellyfish_settings.width,
                             self.jellyfish_settings.height,
                             Vector2(x_pos, y_pos),
                             Vector2(0.0, 0.0),
                             self.jellyfish_settings.max_speed,
                             self.jellyfish_settings.max_acceleration,
                             self.jellyfish_settings.health,
                             self.jellyfish_settings.damage
                         )
                        )
