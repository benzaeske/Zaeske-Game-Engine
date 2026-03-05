from uuid import UUID

from pygame import Surface, Vector2

from model.entities.enemy import Enemy
from model.entities.entity import Entity, FrameActionContext
from model.entities.jellyfishconfig import JellyfishConfig
from model.utils.entityutils import calculate_shortest_distance_and_virtual_position
from model.world.entitygroupindex import EntityGroupIndex


class Jellyfish(Enemy):
    """
    Jellyfish are basic enemies with the added behavior of running away from red fish
    """
    def __init__(
            self,
            sprite: Surface,
            group_id: UUID,
            config: JellyfishConfig,
    ) -> None:
        super().__init__(sprite, group_id, config.enemy_config)
        self._scared_cell_range: int = config.scared_cell_range
        self._scared_dist: float = config.scared_dist
        self._fear_k: float = config.fear_k

    def frame_actions(self, context: FrameActionContext, dt: float) -> None:
        super().frame_actions(context, dt)
        scary_fish: list[Entity] = context.grid_space_access.get_entity_neighbors(
            self,
            self._scared_cell_range,
            context.group_id_query_callback(EntityGroupIndex.RED_FISH)
        )
        # Afraid of red fish
        sum_avoid_fish: Vector2 = Vector2(0.0, 0.0)
        count: int = 0
        for neighbor in scary_fish:
            d, neighbor_pos = calculate_shortest_distance_and_virtual_position(
                self.get_position(), neighbor.get_position(), context.world_specs.world_width
            )
            if 0 < d < self._scared_dist:
                diff: Vector2 = self.get_position() - neighbor_pos
                diff.normalize_ip()
                diff /= d
                sum_avoid_fish += diff
                count += 1
        if count > 0:
            self.target(sum_avoid_fish, self._fear_k)

