from typing import Tuple
from uuid import UUID

from pygame import Surface


from model.entities.fish.fish import Fish
from model.entities.gameentity import GameEntity
from model.entities.jellyfish.jellyfish import Jellyfish


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
        self.contained_entities_by_group: dict[UUID, set[GameEntity]] = {}
        self.background_surface: Surface = background_surface
        # Old
        self.fish: dict[UUID, Fish] = {}
        self.jellyfish: dict[UUID, Jellyfish] = {}


    def add_entity(self, entity: GameEntity):
        if entity.group_id not in self.contained_entities_by_group:
            self.contained_entities_by_group[entity.group_id] = set()
        self.contained_entities_by_group[entity.group_id].add(entity)

    def remove_entity(self, entity: GameEntity):
        if entity.group_id in self.contained_entities_by_group and entity in self.contained_entities_by_group[entity.group_id]:
            self.contained_entities_by_group[entity.group_id].remove(entity)

    def get_contained_entities(self, group_id: UUID) -> set[GameEntity]:
        return self.contained_entities_by_group.get(group_id, set())
