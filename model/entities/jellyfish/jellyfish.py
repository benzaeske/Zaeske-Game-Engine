from pygame import Vector2, Surface

from model.entities.fish.fish import Fish
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

    def update_acceleration(self, player_position: Vector2, neighbors: list[Jellyfish], afraid_neighbors: list[Fish]):
        self.target(player_position - self.position, 1.0)

        # Avoid other jellies when too close
        avoid_jelly_dist: float = 96.0
        avoid_jelly_k: float = 1.0
        sum_avoid_jelly: Vector2 = Vector2(0.0, 0.0)
        count_a_j: int = 0
        for neighbor in neighbors:
            d: float = self.position.distance_to(neighbor.position)
            if (d > 0) and (d < avoid_jelly_dist):
                diff: Vector2 = self.position - neighbor.position
                diff.normalize_ip()
                diff /= d
                sum_avoid_jelly += diff
                count_a_j += 1
        if count_a_j > 0:
            self.target(sum_avoid_jelly, avoid_jelly_k)

        # Afraid of red fish
        afraid_fish_range: float = 256.0
        afraid_fish_k: float = 1.5
        sum_avoid_fish: Vector2 = Vector2(0.0, 0.0)
        count_a_f: int = 0
        for neighbor in afraid_neighbors:
            d: float = self.position.distance_to(neighbor.position)
            if (d > 0) and (d < afraid_fish_range):
                diff: Vector2 = self.position - neighbor.position
                diff.normalize_ip()
                diff /= d
                sum_avoid_fish += diff
                count_a_f += 1
        if count_a_f > 0:
            self.target(sum_avoid_fish, afraid_fish_k)

