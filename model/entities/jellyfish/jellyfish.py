import pygame
from pygame import Surface, Vector2

from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyFishType


class Jellyfish(GameEntity):
    def __init__(self, options: JellyfishSettings):
        super().__init__(
            self.get_jelly_sprite(options.jelly_type, options.width, options.height),
            options.width * 0.75,
            options.height * 0.75,
            options.start_position,
            options.start_velocity,
            options.max_speed,
            options.max_acceleration,
        )
        self.health = options.health
        self.damage = options.damage

    @staticmethod
    def get_jelly_sprite(
        jelly_type: JellyFishType, width: float, height: float
    ) -> Surface:
        match jelly_type:
            case JellyFishType.RED:
                surface: Surface = pygame.image.load(
                    "images/red_jellyfish.png"
                ).convert_alpha()
                return pygame.transform.scale(surface, (width, height))

    def accelerate_towards_player(self, player_position: Vector2):
        self.target(player_position - self.position, 1.0)
