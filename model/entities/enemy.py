from uuid import UUID

from pygame import Surface, Rect, Vector2

from model.entities.enemyconfig import EnemyConfig
from model.entities.entity import Entity, FrameActionContext, EntityMovementContext
from model.entities.physicsentity import PhysicsEntity
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position
from model.world.entitygroupindex import EntityGroupIndex


class Enemy(PhysicsEntity):
    """
    Base class for enemies. Simple logic to accelerate towards the player's position each frame, as well as loose
    avoidance of close neighbors.
    """
    def __init__(
            self,
            sprite: Surface,
            group_id: UUID,
            config: EnemyConfig
    ) -> None:
        super().__init__(sprite, group_id, config.max_speed, config.max_acceleration)
        # The hitbox is how big the entity actually is when performing hit detection.
        # The sprite and the hitbox are on top of each other's centers
        self._hitbox: Rect = Rect(0, 0, config.hitbox_width, config.hitbox_height)
        self._hitbox.center = (int(self.get_x()), int(self.get_y()))
        self._hp: int = config.hp
        self._damage: int = config.damage
        # Constants for calculations performed during frame actions
        self._neighbor_cell_range: int = config.neighbor_cell_range
        self._avoid_neighbor_dist: float = config.avoid_neighbor_k
        self._avoid_neighbor_k: float = config.avoid_neighbor_k

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        world_w: float = context.world_specs.world_width
        self.move_towards_player(context.player.position, world_w)
        neighbors: list[Entity] = context.grid_space_access.get_entity_neighbors(
            self,
            self._neighbor_cell_range,
            context.group_id_query_callback(EntityGroupIndex.ENEMY)
        )
        self.avoid_close_neighbors(neighbors, world_w)

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

    def avoid_close_neighbors(self, neighbors: list[Entity], world_width: float) -> None:
        sum_avoid_neighbors: Vector2 = Vector2(0.0, 0.0)
        count_avoid: int = 0
        for neighbor in neighbors:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.get_position(), neighbor.get_position(), world_width
            )
            if 0 < d < self._avoid_neighbor_dist:
                diff: Vector2 = self._position - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_neighbors += diff
                count_avoid += 1
        if count_avoid > 0:
            self.target(sum_avoid_neighbors, self._avoid_neighbor_k)

    def move(self, context: EntityMovementContext, dt: float) -> None:
        super().move(context, dt)
        self._hitbox.center = (int(self.get_x()), int(self.get_y()))

