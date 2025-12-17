from pygame import Vector2, Surface

from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings


class Jellyfish(GameEntity):
    def __init__(self, jellyfish_sprite: Surface, settings: JellyfishSettings):
        super().__init__(
            jellyfish_sprite,
            settings.width * 0.75,
            settings.height * 0.75,
            settings.start_position,
            settings.start_velocity,
            settings.max_speed,
            settings.max_acceleration,
        )
        self.health = settings.health
        self.damage = settings.damage

    def accelerate_towards_player(self, player_position: Vector2):
        self.target(player_position - self.position, 1.0)
