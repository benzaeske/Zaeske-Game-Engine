import copy
from typing import Callable
from uuid import UUID

import pygame.image
from pygame import Vector2, Surface

from model.entitygroups.entitygroupv1 import EntityGroupV1
from model.entities.fish.fishv1 import FishV1
from model.entities.fish.fishsettingsv1 import FishTypeV1, FishSettingsV1
from model.entities.gameentity import GameEntity
from model.entitygroups.school.schoolparameters import SchoolParameters
from model.world.entitygroupindex import EntityGroupIndex
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class SchoolV1(EntityGroupV1[FishV1]):
    """
    Represents a school of fish. Responsible for creating Fish entities with the given settings passed to it. \n
    All fish created by a school share its school_id
    """

    def __init__(
        self, school_params: SchoolParameters, fish_settings: FishSettingsV1
    ) -> None:
        super().__init__()
        self.school_params: SchoolParameters = school_params
        self.fish_settings: FishSettingsV1 = fish_settings
        self.fish_sprite: Surface = self.load_fish_sprite()

    def update_entities(
        self,
        grid_space: GridSpace,
        get_group_ids_by_type: Callable[[EntityGroupIndex], set[UUID]],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        for current_fish in self._entities:
            neighbors: list[GameEntity] = grid_space.get_entity_neighbors_v1(current_fish, self.school_params.interaction_cell_range)
            current_fish.make_schooling_decisions(
                neighbors,
                self.school_params,
                world_specs.world_width,
                world_specs.world_height,
            )

    def create_entity(self) -> FishV1:
        fish: FishV1 = FishV1(
            copy.deepcopy(self.fish_settings),
            self.group_id,
            self.fish_sprite,
        )
        self.add_entity(fish)
        return fish

    def load_fish_sprite(self) -> Surface:
        match self.fish_settings.fish_type:
            case FishTypeV1.RED:
                surface = pygame.image.load("images/red_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishTypeV1.GREEN:
                surface = pygame.image.load("images/green_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishTypeV1.YELLOW:
                surface = pygame.image.load("images/yellow_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
