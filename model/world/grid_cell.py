from typing import Tuple
from uuid import UUID

import pygame
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
        self.fish: dict[UUID, Fish] = {}
        self.jellyfish: dict[UUID, Jellyfish] = {}
        self.contained_entities_by_group: dict[UUID, set[UUID]] = {}
        self.background_surface: Surface = background_surface

    def add_entity(self, entity: GameEntity):
        if entity.group_id not in self.contained_entities_by_group:
            self.contained_entities_by_group[entity.group_id] = set()
        self.contained_entities_by_group[entity.group_id].add(entity.entity_id)

    def remove_entity(self, entity: GameEntity):
        if entity.group_id in self.contained_entities_by_group and entity.entity_id in self.contained_entities_by_group[entity.group_id]:
            self.contained_entities_by_group[entity.group_id].remove(entity.entity_id)
            if len(self.contained_entities_by_group.get(entity.group_id)) is 0:
                self.contained_entities_by_group.pop(entity.group_id)

    def get_contained_entity_ids_by_group(self, group_id: UUID) -> set[UUID]:
        return self.contained_entities_by_group.get(group_id, set())
