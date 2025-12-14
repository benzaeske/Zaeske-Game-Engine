from pygame import Vector2, Surface

from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings


class Jellyfish(GameEntity):
    def __init__(self, jellyfish_sprite: Surface, options: JellyfishSettings):
        super().__init__(
            jellyfish_sprite,
            options.width * 0.75,
            options.height * 0.75,
            options.start_position,
            options.start_velocity,
            options.max_speed,
            options.max_acceleration,
        )
        self.health = options.health
        self.damage = options.damage

    def accelerate_towards_player(self, player_position: Vector2):
        self.target(player_position - self.position, 1.0)
