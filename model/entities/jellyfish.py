from uuid import UUID

from pygame import Surface, Vector2

from model.entities.enemy import Enemy
from model.entities.enemyconfig import EnemyConfig
from model.entities.entity import Entity
from model.entities.jellyfishconfig import JellyfishConfig
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position


class Jellyfish(Enemy):
    """
    Jellyfish are vampire-survivors-type enemies with the added behavior of running away from red fish.
    """
    def __init__(
            self,
            sprite: Surface,
            manager_id: UUID,
            enemy_config: EnemyConfig,
    ) -> None:
        super().__init__(sprite, manager_id, enemy_config)

    def avoid_fish(
            self,
            jelly_config: JellyfishConfig,
            avoid_fish: list[Entity],
            world_w: float
    ) -> None:
        sum_avoid_fish: Vector2 = Vector2(0.0, 0.0)
        count: int = 0
        for neighbor in avoid_fish:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.get_position(), neighbor.get_position(), world_w
            )
            if 0 < d < jelly_config.scared_dist:
                diff: Vector2 = self.get_position() - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_fish += diff
                count += 1
        if count > 0:
            self.target(sum_avoid_fish, jelly_config.fear_k)

