from uuid import UUID

from pygame import Vector2

from model.entitygroups.entitygroup import EntityGroup
from model.entities.gameentity import GameEntity
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class EntityManager:
    """
    A global entity manager. Stores all entities that are currently loaded into the game
    """
    def __init__(self):
        self._entity_groups: dict[UUID, EntityGroup] = {}

    def add_entity_group(self, entity_group: EntityGroup) -> None:
        self._entity_groups[entity_group.group_id] = entity_group

    def remove_entity_group(self, group_id: UUID) -> None:
        self._entity_groups.pop(group_id)

    def add_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].add_entity(entity)

    def remove_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].remove_entity(entity)

    def update_all_groups(self, world_specs: WorldSpecs, grid_space: GridSpace, player_position: Vector2) -> None:
        for group in self._entity_groups.values():
            # TODO update group impls to use GridSpace class
            group.update_entities(world_specs, grid_space, self._entity_groups, player_position)

    def move_all_groups(self, world_specs: WorldSpecs, grid_space: GridSpace, dt: float):
        for group in self._entity_groups.values():
            # TODO update group impls to use GridSpace class
            group.move_entities(world_specs, grid_space, dt)

