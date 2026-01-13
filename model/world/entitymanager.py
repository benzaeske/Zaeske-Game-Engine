from uuid import UUID

from model.entitygroups.entitygroup import EntityGroup
from model.entities.gameentity import GameEntity


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

