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

    def update_acceleration(self, player_position: Vector2, neighbors: list[Jellyfish]):
        self.target(player_position - self.position, 1.0)

        # Avoid other jellies when too close
        avoid_distance: float = 96.0
        avoid_k: float = 1.0
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        count_a: int = 0
        for neighbor in neighbors:
            d: float = self.position.distance_to(neighbor.position)
            if (d > 0) and (d < avoid_distance):
                diff: Vector2 = self.position - neighbor.position
                diff.normalize_ip()
                diff /= d
                sum_avoid += diff
                count_a += 1
        if count_a > 0:
            self.target(sum_avoid, avoid_k)

