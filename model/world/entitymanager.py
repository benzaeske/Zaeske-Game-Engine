from uuid import UUID

from pygame import Vector2

from model.entities.fish.fishsettings import FishType
from model.entitygroups.entitygroup import EntityGroup
from model.entities.gameentity import GameEntity
from model.entitygroups.jellyfishswarm.jellyfishswarm import JellyfishSwarm
from model.entitygroups.school.school import School
from model.world.entitygroupindex import EntityGroupIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs

class EntityManager:
    """
    A global entity manager. Stores all entities that are currently loaded into the game
    """
    def __init__(self):
        self._entity_groups: dict[UUID, EntityGroup] = {}
        # Maintain sets of EntityGroup ids keyed by the various types defined in the EntityGroupIndex Enum.
        self._indexed_group_ids: dict[EntityGroupIndex, set[UUID]] = {index: set() for index in EntityGroupIndex}

    def update_all_groups(self, grid_space: GridSpace, world_specs: WorldSpecs, player_position: Vector2) -> None:
        for group in self._entity_groups.values():
            group.update_entities(grid_space, self.get_group_ids_by_type, world_specs, player_position)

    def move_all_groups(self, grid_space: GridSpace, world_specs: WorldSpecs, dt: float):
        for group in self._entity_groups.values():
            group.move_entities(grid_space, world_specs, dt)

    def add_entity_group(self, entity_group: EntityGroup) -> None:
        self._entity_groups[entity_group.group_id] = entity_group
        self._index_entity_group(entity_group)

    def remove_entity_group(self, group_id: UUID) -> None:
        self._entity_groups.pop(group_id)
        # Remove the group id from any indexes it was associated with
        for index, ids in self._indexed_group_ids.items():
            if group_id in ids:
                ids.remove(group_id)

    def _index_entity_group(self, entity_group: EntityGroup) -> None:
        if isinstance(entity_group, JellyfishSwarm):
            self._indexed_group_ids[EntityGroupIndex.JELLY].add(entity_group.group_id)
        elif isinstance(entity_group, School):
            match entity_group.fish_settings.fish_type:
                case FishType.RED:
                    self._indexed_group_ids[EntityGroupIndex.RED_FISH].add(entity_group.group_id)
                case FishType.YELLOW:
                    self._indexed_group_ids[EntityGroupIndex.YELLOW_FISH].add(entity_group.group_id)
                case FishType.GREEN:
                    self._indexed_group_ids[EntityGroupIndex.GREEN_FISH].add(entity_group.group_id)

    def get_entity_group(self, group_id: UUID) -> EntityGroup:
        return self._entity_groups[group_id]

    def get_group_ids_by_type(self, entity_type: EntityGroupIndex) -> set[UUID]:
        return self._indexed_group_ids.get(entity_type, set())

    def add_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].add_entity(entity)

    def remove_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].remove_entity(entity)

