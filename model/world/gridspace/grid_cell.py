from typing import Tuple
from uuid import UUID

from model.entity.entity import Entity


class GridCell:
    """
    An individual grid cell in the model's grid space.
    """
    def __init__(
        self,
        coordinate: Tuple[int, int]
    ):
        self._coordinate: Tuple[int, int] = coordinate
        self._contained_entities_by_manager_id: dict[UUID, set[Entity]] = {}

    def add_entity(self, entity: Entity):
        if entity.manager_id not in self._contained_entities_by_manager_id:
            self._contained_entities_by_manager_id[entity.manager_id] = set()
        self._contained_entities_by_manager_id[entity.manager_id].add(entity)

    def remove_entity(self, entity: Entity):
        if entity.manager_id in self._contained_entities_by_manager_id and entity in self._contained_entities_by_manager_id[entity.manager_id]:
            self._contained_entities_by_manager_id[entity.manager_id].remove(entity)

    def get_entities_by_manager_id(self, manager_id: UUID) -> set[Entity]:
        return self._contained_entities_by_manager_id.get(manager_id, set())

    def get_entities_by_manager_ids(self, manager_ids: set[UUID]) -> set[Entity]:
        entities: set[Entity] = set()
        for group_id in manager_ids:
            entities.update(self._contained_entities_by_manager_id.get(group_id, set()))
        return entities
