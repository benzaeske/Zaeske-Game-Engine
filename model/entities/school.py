import random
import uuid
from uuid import UUID

import pygame.image
from pygame import Vector2, Surface, Rect

from model.entities.fish import FishSettings, Fish, FishType
from model.utils.vectorutils import limit_magnitude


class SchoolParameters:

    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        interaction_cell_range: int,
        cohere_k: float,
        avoid_k: float,
        align_k: float,
        shoal_location: Vector2 | None,
        shoal_radius: float,
        shoal_k: float,
        hatch_region: Rect,
        egg_count: int,
    ) -> None:
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.interaction_cell_range: int = interaction_cell_range
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k
        self.shoal_location: Vector2 = shoal_location
        self.shoal_radius: float = shoal_radius
        self.shoal_k: float = shoal_k
        self.hatch_region: Rect = hatch_region
        self.egg_count: int = egg_count


class School:
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
            self.fish_settings.max_speed, self.fish_settings.max_speed
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
