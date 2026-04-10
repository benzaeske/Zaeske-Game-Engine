from copy import copy
from uuid import UUID

from pygame import Rect, Vector2

from model.entities.enemies.enemyconfig import EnemyConfig
from model.entities.physicsentity import PhysicsEntity
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Enemy(PhysicsEntity):
    """
    Base class for vampire-survivors-type enemies. Simple logic to accelerate towards the player's position each frame
    while loosely avoiding close neighbors.
    """
    def __init__(
            self,
            config: EnemyConfig,
            manager_id: UUID,
    ) -> None:
        super().__init__(config, manager_id)
        # The hitbox is how big the entity actually is when performing hit detection.
        # Can be different from sprite dimensions
        self._hitbox: Rect = Rect(0, 0, config.hitbox_width, config.hitbox_height)
        self.sync_hitbox_position()
        self._neighbor_cell_range: int = config.neighbor_cell_range
        self._avoid_neighbor_dist: float = config.avoid_neighbor_dist
        self._avoid_neighbor_k: float = config.avoid_neighbor_k
        self._hp: float = config.hp
        self._damage: float = config.damage
        # Optional fear behavior:
        self._is_afraid: bool = config.is_afraid
        self._afraid_of_index: EntityManagerIndex = config.afraid_of_index
        self._scared_cell_range: int = config.scared_cell_range
        self._scared_dist: float = config.scared_dist
        self._scared_k: float = config.scared_k

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        self._move_towards_player(context)
        self._avoid_close_neighbors(context)
        if self._is_afraid:
            self._fear(context)

    def _move_towards_player(self, context: ModelContext) -> None:
        self.target(context.player.get_position() - self.get_position(), 1.0)

    def _avoid_close_neighbors(self, context: ModelContext) -> None:
        sum_avoid_neighbors: Vector2 = Vector2(0.0, 0.0)
        count_avoid: int = 0
        for neighbor in context.grid_space.get_neighbors_for_entity(self, self._neighbor_cell_range,
                                                                    context.entity_repository.get_manager_ids(EntityManagerIndex.ENEMY)):
            d: float = self.get_position().distance_to(neighbor.get_position())
            if 0 < d < self._avoid_neighbor_dist:
                diff: Vector2 = self._position - neighbor.get_position()
                diff.normalize_ip()
                diff /= d
                sum_avoid_neighbors += diff
                count_avoid += 1
        if count_avoid > 0:
            self.target(sum_avoid_neighbors, self._avoid_neighbor_k)

    def _fear(self, context: ModelContext) -> None:
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        count: int = 0
        neighbors = context.grid_space.get_neighbors_for_entity(self, self._scared_cell_range,
                                                                    context.entity_repository.get_manager_ids(self._afraid_of_index))
        for neighbor in neighbors:
            d: float = self.get_position().distance_to(neighbor.get_position())
            if 0 < d < self._scared_dist:
                diff: Vector2 = self.get_position() - neighbor.get_position()
                diff.normalize_ip()
                diff /= d
                sum_avoid += diff
                count += 1
        if count > 0:
            self.target(sum_avoid, self._scared_k)

    def move(self, context: ModelContext, dt: float) -> None:
        super().move(context, dt)
        self.sync_hitbox_position()

    def sync_hitbox_position(self) -> None:
        """
        Syncs this enemy's hitbox center with its position vector
        """
        self._hitbox.center = self.get_position()

    def get_hitbox(self) -> Rect:
        """
        Read only. Returns a shallow copy of the current rectangular hitbox.
        """
        return copy(self._hitbox)

    def get_hp(self) -> float:
        return self._hp

    def update_hp(self, hp_diff: float) -> None:
        """
        Adds the given value to this enemy's hp
        """
        self._hp += hp_diff

    def get_damage(self) -> float:
        return self._damage