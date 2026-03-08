from uuid import UUID

from pygame import Vector2

from model.entities.enemy import Enemy
from model.entities.fish.fishsettingsv1 import FishTypeV1
from model.entitymanagers.entitygroupv1 import EntityGroupV1
from model.entities.gameentity import GameEntity
from model.entitymanagers.jellyfishswarmfolder.jellyfishswarmv1 import JellyfishSwarmV1
from model.entitymanagers.schoolfolder.schoolv1 import SchoolV1
from model.world.entityrepository.entitymanagerindex import EntityManagerIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs

class EntityManagerV1:
    """
    A global entity manager. Stores all entities that are currently loaded into the game.
    Contains functions to easily query existing EntityGroups and GameEntities.
    """
    def __init__(self):
        self._entity_groups: dict[UUID, EntityGroupV1] = {}
        # Maintain sets of EntityGroup ids keyed by the various types defined in the EntityGroupIndex Enum.
        self._indexed_group_ids: dict[EntityManagerIndex, set[UUID]] = {index: set() for index in EntityManagerIndex}

    def update_all_groups(self, grid_space: GridSpace, world_specs: WorldSpecs, player_position: Vector2) -> None:
        for group in self._entity_groups.values():
            group.update_entities(grid_space, self.get_group_ids_by_type, world_specs, player_position)

    def move_all_groups(self, grid_space: GridSpace, world_specs: WorldSpecs, dt: float):
        for group in self._entity_groups.values():
            group.move_entities(grid_space, world_specs, dt)

    def add_entity_group(self, entity_group: EntityGroupV1) -> None:
        self._entity_groups[entity_group.group_id] = entity_group
        self._index_entity_group(entity_group)

    def remove_entity_group(self, group_id: UUID) -> None:
        self._entity_groups.pop(group_id)
        # Remove the group id from any indexes it was associated with
        for index, ids in self._indexed_group_ids.items():
            if group_id in ids:
                ids.remove(group_id)

    def _index_entity_group(self, entity_group: EntityGroupV1) -> None:
        if isinstance(entity_group, JellyfishSwarmV1):
            self._indexed_group_ids[EntityManagerIndex.JELLY].add(entity_group.group_id)
        elif isinstance(entity_group, Enemy):
            self._indexed_group_ids[EntityManagerIndex.ENEMY].add(entity_group.manager_id)
        elif isinstance(entity_group, SchoolV1):
            match entity_group.fish_settings.fish_type:
                case FishTypeV1.RED:
                    self._indexed_group_ids[EntityManagerIndex.RED_FISH].add(entity_group.group_id)
                case FishTypeV1.YELLOW:
                    self._indexed_group_ids[EntityManagerIndex.YELLOW_FISH].add(entity_group.group_id)
                case FishTypeV1.GREEN:
                    self._indexed_group_ids[EntityManagerIndex.GREEN_FISH].add(entity_group.group_id)

    def get_entity_group(self, group_id: UUID) -> EntityGroupV1:
        return self._entity_groups[group_id]

    def get_group_ids_by_type(self, entity_type: EntityManagerIndex) -> set[UUID]:
        return self._indexed_group_ids.get(entity_type, set())

    def add_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].add_entity(entity)

    def remove_entity(self, entity: GameEntity) -> None:
        self._entity_groups[entity.group_id].remove_entity(entity)

