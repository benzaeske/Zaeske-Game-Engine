from typing import Tuple
from uuid import UUID

from pygame import Surface


from model.entities.gameentity import GameEntity


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
        self.contained_entities_by_group_id: dict[UUID, set[GameEntity]] = {}
        self.background_surface: Surface = background_surface

    def add_entity(self, entity: GameEntity):
        if entity.group_id not in self.contained_entities_by_group_id:
            self.contained_entities_by_group_id[entity.group_id] = set()
        self.contained_entities_by_group_id[entity.group_id].add(entity)

    def remove_entity(self, entity: GameEntity):
        if entity.group_id in self.contained_entities_by_group_id and entity in self.contained_entities_by_group_id[entity.group_id]:
            self.contained_entities_by_group_id[entity.group_id].remove(entity)

    def get_entities_by_group_id(self, group_id: UUID) -> set[GameEntity]:
        return self.contained_entities_by_group_id.get(group_id, set())

    def get_entities_by_group_ids(self, group_ids: set[UUID]) -> set[GameEntity]:
        entities: set[GameEntity] = set()
        for group_id in group_ids:
            entities.update(self.contained_entities_by_group_id.get(group_id, set()))
        return entities
