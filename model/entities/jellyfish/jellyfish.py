from pygame import Vector2, Surface

from model.entities.fish.fish import Fish
from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position


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

    def update_acceleration(
        self,
        player_position: Vector2,
        neighbors: list["Jellyfish"],
        afraid_neighbors: list[Fish],
        world_width: float,
    ):
        self.move_towards_player(player_position, world_width)
        self.avoid_close_neighbors(neighbors, world_width)
        self.run_away_from_fish(afraid_neighbors, world_width)

    def move_towards_player(self, player_position: Vector2, world_width: float) -> None:
        direct_diff_x = player_position.x - self.position.x
        wrap_diff_x = (
            (direct_diff_x - world_width)
            if self.position.x < (world_width / 2)
            else (direct_diff_x + world_width)
        )
        if abs(direct_diff_x) < abs(wrap_diff_x):
            self.target(
                Vector2(direct_diff_x, player_position.y - self.position.y), 1.0
            )
        else:
            self.target(Vector2(wrap_diff_x, player_position.y - self.position.y), 1.0)

    def avoid_close_neighbors(self, neighbors: list["Jellyfish"], world_width: float):
        avoid_jelly_dist: float = 96.0
        avoid_jelly_k: float = 2.0
        sum_avoid_jelly: Vector2 = Vector2(0.0, 0.0)
        count_avoid: int = 0
        for neighbor in neighbors:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.position, neighbor.position, world_width
            )
            if 0 < d < avoid_jelly_dist:
                diff: Vector2 = self.position - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_jelly += diff
                count_avoid += 1
        if count_avoid > 0:
            self.target(sum_avoid_jelly, avoid_jelly_k)

    def run_away_from_fish(
        self, afraid_neighbors: list[Fish], world_width: float
    ) -> None:
        # Afraid of red fish
        scared_range: float = 192.0
        fear_k: float = 3.0
        sum_avoid_fish: Vector2 = Vector2(0.0, 0.0)
        count: int = 0
        for neighbor in afraid_neighbors:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.position, neighbor.position, world_width
            )
            if 0 < d < scared_range:
                diff: Vector2 = self.position - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_fish += diff
                count += 1
        if count > 0:
            self.target(sum_avoid_fish, fear_k)
