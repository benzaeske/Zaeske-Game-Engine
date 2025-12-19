import random
import uuid
from uuid import UUID

import pygame.image
from pygame import Vector2, Surface

from model.entities.fish.fish import Fish
from model.entities.fish.fishsettings import FishType, FishSettings
from model.entities.school.schoolparameters import SchoolParameters
from model.utils.vectorutils import limit_magnitude


class School:
    """
    Represents a school of fish. Responsible for creating Fish entities with the given settings passed to it. \n
    All fish created by a school share its school_id
    """

    def __init__(
        self,
        school_params: SchoolParameters,
        fish_settings: FishSettings,
    ) -> None:
        self.school_id: UUID = uuid.uuid4()
        self.school_params: SchoolParameters = school_params
        self.fish_settings: FishSettings = fish_settings
        self.fish_sprite: Surface = self.load_fish_sprite()

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
        hatch_region = self.school_params.hatch_region
        initial_position = Vector2(
            random.uniform(hatch_region.x, hatch_region.x + hatch_region.width),
            random.uniform(hatch_region.y, hatch_region.y + hatch_region.height),
        )
        initial_velocity = Vector2(
            random.uniform(-self.fish_settings.max_speed, self.fish_settings.max_speed),
            random.uniform(-self.fish_settings.max_speed, self.fish_settings.max_speed)
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
            self.school_id,
            self.fish_sprite,
        )
