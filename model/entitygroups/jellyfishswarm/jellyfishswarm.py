import random
from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.gameentity import GameEntity
from model.entitygroups.entitygroup import EntityGroup
from model.entities.fish.fishsettings import FishType
from model.entities.jellyfish.jellyfish import Jellyfish
from model.entities.jellyfish.jellyfishsettings import JellyfishSettings, JellyfishType
from model.entitygroups.school.school import School
from model.player.cameraspecs import CameraSpecs
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class JellyfishSwarm(EntityGroup[Jellyfish]):
    def __init__(self, jellyfish_settings: JellyfishSettings, amount: int):
        super().__init__()
        self.jellyfish_settings: JellyfishSettings = jellyfish_settings
        self.sprite = self.get_jelly_sprite(
            jellyfish_settings.jelly_type,
            jellyfish_settings.width,
            jellyfish_settings.height,
        )
        self.amount: int = amount

    def update_entities(
        self,
        grid_space: GridSpace,
        entity_groups: dict[UUID, EntityGroup],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        # TODO make these properties on jellyfish settings
        neighbor_range: int = 1
        scared_range: int = 2
        scared_of_groups: set[UUID] = self.get_scared_group_ids(entity_groups)
        for jellyfish in self._entities:
            neighbor_jellies: list[GameEntity] = grid_space.get_neighbors(jellyfish, neighbor_range)
            afraid_of_fish: list[GameEntity] = grid_space.get_neighbors(jellyfish, scared_range, scared_of_groups)
            jellyfish.update_acceleration(
                player_position,
                neighbor_jellies,
                afraid_of_fish,
                world_specs.world_width,
            )

    @staticmethod
    def get_scared_group_ids(entity_groups: dict[UUID, EntityGroup]) -> set[UUID]:
        """
        Returns a set of group ids of entities that jellyfish are afraid of
        :param entity_groups: The current entity groups present in the game world
        :return: A set of group ids
        """
        scared_of_groups: set[UUID] = set()
        for group in entity_groups.values():
            if isinstance(group, School) and group.fish_settings.fish_type is FishType.RED:
                scared_of_groups.add(group.group_id)
        return scared_of_groups

    def create_entity(self) -> Jellyfish:
        jelly: Jellyfish = Jellyfish(
            self.group_id,
            self.sprite,
            JellyfishSettings(
                self.jellyfish_settings.jelly_type,
                self.jellyfish_settings.width,
                self.jellyfish_settings.height,
                self.jellyfish_settings.max_speed,
                self.jellyfish_settings.max_acceleration,
                self.jellyfish_settings.health,
                self.jellyfish_settings.damage,
            )
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
