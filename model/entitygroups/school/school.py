import random
from typing import Callable
from uuid import UUID

import pygame.image
from pygame import Vector2, Surface

from model.entitygroups.entitygroup import EntityGroup
from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType, FishSettings
from model.entities.gameentity import GameEntity
from model.entitygroups.school.schoolparameters import SchoolParameters
from model.player.cameraspecs import CameraSpecs
from model.utils.vectorutils import limit_magnitude
from model.world.gridspace import GridSpace
from model.world.worldspecs import WorldSpecs


class School(EntityGroup[Fish]):
    """
    Represents a school of fish. Responsible for creating Fish entities with the given settings passed to it. \n
    All fish created by a school share its school_id
    """

    def __init__(
        self, school_params: SchoolParameters, fish_settings: FishSettings
    ) -> None:
        super().__init__()
        self.school_params: SchoolParameters = school_params
        self.fish_settings: FishSettings = fish_settings
        self.fish_sprite: Surface = self.load_fish_sprite()

    def update_entities(
        self,
        grid_space: GridSpace,
        entity_groups: dict[UUID, EntityGroup],
        world_specs: WorldSpecs,
        player_position: Vector2 | None = None,
    ) -> None:
        for current_fish in self._entities:
            neighbors: list[GameEntity] = grid_space.get_neighbors(current_fish, self.school_params.interaction_cell_range)
            current_fish.make_schooling_decisions(
                neighbors,
                self.school_params,
                world_specs.world_width,
                world_specs.world_height,
            )

    def create_entity(
        self,
        world_specs: WorldSpecs,
        camera_specs: CameraSpecs | None = None,
        camera_position: Vector2 | None = None,
    ) -> GameEntity:
        return self.hatch_fish()

    def load_fish_sprite(self) -> Surface:
        match self.fish_settings.fish_type:
            case FishType.RED:
                surface = pygame.image.load("images/red_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishType.GREEN:
                surface = pygame.image.load("images/green_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishType.YELLOW:
                surface = pygame.image.load("images/yellow_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )

    def hatch_fish(self) -> Fish:
        # TODO this should only create a new fish with a naive starting position.
        #  Logic for positioning the fish should live in the spawner impl
        hatch_region = self.school_params.hatch_region
        initial_position = Vector2(
            random.uniform(hatch_region.x, hatch_region.x + hatch_region.width),
            random.uniform(hatch_region.y, hatch_region.y + hatch_region.height),
        )
        initial_velocity = Vector2(
            random.uniform(-self.fish_settings.max_speed, self.fish_settings.max_speed),
            random.uniform(-self.fish_settings.max_speed, self.fish_settings.max_speed),
        )
        limit_magnitude(initial_velocity, self.fish_settings.max_speed)
        return Fish(
            FishSettings(
                self.fish_settings.fish_type,
                self.fish_settings.width,
                self.fish_settings.height,
                self.fish_settings.max_speed,
                self.fish_settings.max_acceleration,
                initial_position,
                initial_velocity,
            ),
            self.group_id,
            self.fish_sprite,
        )
