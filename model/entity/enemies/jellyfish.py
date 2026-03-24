from uuid import UUID

from pygame import Vector2

from model.entity.enemies.enemy import Enemy
from model.entity.enemies.jellyfishconfig import JellyfishConfig
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.modelcontext import ModelContext


class Jellyfish(Enemy):
    """
    Jellyfish are vampire-survivors-type enemies with the added behavior of running away from red fish.
    """
    def __init__(
            self,
            manager_id: UUID,
            config: JellyfishConfig
    ) -> None:
        super().__init__(manager_id, config.enemy_config)
        self._scared_cell_range: int = config.scared_cell_range
        self._scared_dist: float = config.scared_dist
        self._fear_k: float = config.fear_k

    def frame_actions(self, context: ModelContext, dt: float) -> None:
        super().frame_actions(context, dt)
        self._avoid_fish(context)

    def _avoid_fish(self, context: ModelContext) -> None:
        sum_avoid_fish: Vector2 = Vector2(0.0, 0.0)
        count: int = 0
        for neighbor in context.grid_space.get_neighbors_for_entity(self, self._scared_cell_range,
                                                                    context.entity_repository.get_manager_ids(EntityManagerIndex.RED_FISH)):
            d: float = self.get_position().distance_to(neighbor.get_position())
            if 0 < d < self._scared_dist:
                diff: Vector2 = self.get_position() - neighbor.get_position()
                diff.normalize_ip()
                diff /= d
                sum_avoid_fish += diff
                count += 1
        if count > 0:
            self.target(sum_avoid_fish, self._fear_k)