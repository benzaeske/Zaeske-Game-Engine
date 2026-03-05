from uuid import UUID

from pygame import Surface, Rect, Vector2

from model.entities.enemyconfig import EnemyConfig
from model.entities.entity import Entity
from model.entities.physicsentity import PhysicsEntity
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position


class Enemy(PhysicsEntity):
    """
    Base class for vampire-survivors-type enemies. Simple logic to accelerate towards the player's position each frame
    while loosely avoiding close neighbors.
    """
    def __init__(
            self,
            sprite: Surface,
            manager_id: UUID,
            config: EnemyConfig
    ) -> None:
        super().__init__(sprite, manager_id, config.max_speed, config.max_acceleration)
        # The hitbox is how big the entity actually is when performing hit detection.
        # The sprite and the hitbox are on top of each other's centers
        self._hitbox: Rect = Rect(0, 0, config.hitbox_width, config.hitbox_height)
        self._hitbox.center = (int(self.get_x()), int(self.get_y()))
        self._hp: float = config.hp
        self._damage: float = config.damage

    def swarm_to_player(
            self,
            enemy_config: EnemyConfig,
            player_position: Vector2,
            neighbors: list[Entity],
            world_w: float
    ) -> None:
        self.move_towards_player(player_position, world_w)
        self.avoid_close_neighbors(enemy_config, neighbors, world_w)

    def move_towards_player(self, player_position: Vector2, world_width: float) -> None:
        direct_diff_x = player_position.x - self.get_x()
        wrap_diff_x = (
            (direct_diff_x - world_width)
            if self.get_x() < (world_width / 2)
            else (direct_diff_x + world_width)
        )
        if abs(direct_diff_x) < abs(wrap_diff_x):
            self.target(
                Vector2(direct_diff_x, player_position.y - self.get_y()), 1.0
            )
        else:
            self.target(Vector2(wrap_diff_x, player_position.y - self.get_y()), 1.0)

    def avoid_close_neighbors(
            self,
            enemy_config: EnemyConfig,
            neighbors: list[Entity],
            world_width: float
    ) -> None:
        sum_avoid_neighbors: Vector2 = Vector2(0.0, 0.0)
        count_avoid: int = 0
        for neighbor in neighbors:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.get_position(), neighbor.get_position(), world_width
            )
            if 0 < d < enemy_config.avoid_neighbor_dist:
                diff: Vector2 = self._position - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_neighbors += diff
                count_avoid += 1
        if count_avoid > 0:
            self.target(sum_avoid_neighbors, enemy_config.avoid_neighbor_k)

    def move(self, world_w: float, world_h: float, dt: float) -> None:
        super().move(world_w, world_h, dt)
        self._hitbox.center = (int(self.get_x()), int(self.get_y()))

    def get_hitbox(self) -> Rect:
        return self._hitbox

    def get_hp(self) -> float:
        return self._hp

    def get_damage(self) -> float:
        return self._damage

    def take_damage(self, n: float) -> None:
        """
        Subtracts the provided value from the enemy's hp
        """
        self._hp -= n

    def heal(self, n: float) -> None:
        """
        Adds the provided value to the enemy's hp
        """
        self._hp += n



