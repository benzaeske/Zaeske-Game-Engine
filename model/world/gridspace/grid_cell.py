from typing import Tuple
from uuid import UUID

from pygame import Surface

from model.entities.entity import Entity


class GridCell:
    """
    An individual grid cell in the model's grid space.
    """
    def __init__(
        self,
        coordinates: Tuple[int, int],
        background_surface: Surface,
    ):
        self.coordinates: Tuple[int, int] = coordinates
        self.contained_entities_by_manager_id: dict[UUID, set[Entity]] = {}
        self.background_surface: Surface = background_surface

    def add_entity(self, entity: Entity):
        if entity.manager_id not in self.contained_entities_by_manager_id:
            self.contained_entities_by_manager_id[entity.manager_id] = set()
        self.contained_entities_by_manager_id[entity.manager_id].add(entity)

    def remove_entity(self, entity: Entity):
        if entity.manager_id in self.contained_entities_by_manager_id and entity in self.contained_entities_by_manager_id[entity.manager_id]:
            self.contained_entities_by_manager_id[entity.manager_id].remove(entity)

    def get_entities_by_manager_id(self, manager_id: UUID) -> set[Entity]:
        return self.contained_entities_by_manager_id.get(manager_id, set())

    def get_entities_by_manager_ids(self, manager_ids: set[UUID]) -> set[Entity]:
        entities: set[Entity] = set()
        for group_id in manager_ids:
            entities.update(self.contained_entities_by_manager_id.get(group_id, set()))
        return entities
