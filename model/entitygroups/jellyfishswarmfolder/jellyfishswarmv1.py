import copy
from typing import Callable
from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.gameentity import GameEntity
from model.entitygroups.entitygroupv1 import EntityGroupV1
from model.entities.jellyfishfolder.jellyfishv1 import JellyfishV1
from model.entities.jellyfishfolder.jellyfishsettingsv1 import JellyfishSettingsV1, JellyfishType
from model.world.entitymanagerindex import EntityManagerIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class JellyfishSwarmV1(EntityGroupV1[JellyfishV1]):
    def __init__(self, jellyfish_settings: JellyfishSettingsV1, amount: int):
        super().__init__()
        self.jellyfish_settings: JellyfishSettingsV1 = jellyfish_settings
        self.sprite = self.get_jelly_sprite(
            jellyfish_settings.jelly_type,
            jellyfish_settings.width,
            jellyfish_settings.height,
        )
        self.amount: int = amount

    def update_entities(
        self,
        grid_space: GridSpace,
        get_group_ids_by_type: Callable[[EntityManagerIndex], set[UUID]],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        scared_of_groups: set[UUID] = get_group_ids_by_type(EntityManagerIndex.RED_FISH)
        for jellyfish in self._entities:
            neighbor_jellies: list[GameEntity] = grid_space.get_entity_neighbors_v1(jellyfish, self.jellyfish_settings.neighbor_range)
            afraid_of_fish: list[GameEntity] = grid_space.get_entity_neighbors_v1(jellyfish, self.jellyfish_settings.scared_range, scared_of_groups)
            jellyfish.update_acceleration(
                player_position,
                neighbor_jellies,
                afraid_of_fish,
                world_specs.world_width,
            )

    def create_entity(self) -> JellyfishV1:
        jelly: JellyfishV1 = JellyfishV1(
            self.group_id,
            self.sprite,
            copy.deepcopy(self.jellyfish_settings)
        )
        self.add_entity(jelly)
        return jelly

    @staticmethod
    def get_jelly_sprite(
        jelly_type: JellyfishType, width: float, height: float
    ) -> Surface:
        match jelly_type:
            case JellyfishType.RED:
                surface: Surface = pygame.image.load(
                    "images/red_jelly.png"
                ).convert_alpha()
                return pygame.transform.scale(surface, (width, height))
