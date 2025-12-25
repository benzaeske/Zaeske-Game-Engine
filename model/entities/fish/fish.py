import math
from uuid import UUID

import pygame
from pygame import Vector2, Surface

from model.entities.fish.fishsettings import FishSettings
from model.entities.gameentity import GameEntity
from model.entities.school.schoolparameters import SchoolParameters


class Fish(GameEntity):
    """
    A fish entity with functions for applying boid's algorithm each frame to mimic schooling behavior
    """

    def __init__(
        self,
        fish_settings: FishSettings,
        school_id: UUID,
        fish_sprite: Surface,
    ) -> None:
        self.school_id: UUID = school_id
        super().__init__(
            fish_sprite,
            fish_settings.width,
            fish_settings.height,
            fish_settings.initial_position,
            fish_settings.initial_velocity,
            fish_settings.max_speed,
            fish_settings.max_acceleration,
        )

    def make_schooling_decisions(
        self, others: list["Fish"], school_params: SchoolParameters, world_width: float
    ) -> None:
        self._school(others, school_params, world_width)
        if school_params.shoal_location is not None:
            self._shoal(school_params, world_width)

    def _school(self, others: list["Fish"], school_params: SchoolParameters, world_width: float) -> None:
        """
        Applies acceleration to this fish according to three rules for schooling\n
        #. Each fish moves away from other fish that are within its avoidance range.\n
        #. Each fish aligns its velocity with other fish in its coherence range.\n
        #. Each fish moves towards the average position of other fish in its coherence range.\n
        :param others: Other fish that are within a relevant distance of this one
        :param school_params: Parameters for controlling schooling decisions
        """
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for other in others:
            if self.school_id == other.school_id and self.uuid != other.uuid:
                direct_d: float = self.position.distance_to(other.position)
                wrap_pos: Vector2 = other.position + Vector2(world_width, 0) if other.position.x < (world_width / 2) else other.position - Vector2(world_width, 0)
                wrap_d: float = self.position.distance_to(wrap_pos)
                other_pos = other.position
                d = direct_d
                if wrap_d < direct_d:
                    other_pos = wrap_pos
                    d = wrap_d
                if 0 < d < school_params.cohere_distance:
                    sum_align += other.velocity
                    sum_cohere += other_pos
                    count_n += 1
                if 0 < d < school_params.avoid_distance:
                    diff: Vector2 = self.position - other_pos
                    diff.normalize_ip()
                    diff /= d
                    sum_avoid += diff
                    count_s += 1
        if count_s > 0:
            self.target(sum_avoid, school_params.avoid_k)
        if count_n > 0:
            self.target(sum_align, school_params.align_k)
            sum_cohere /= float(count_n)
            sum_cohere -= self.position
            self.target(sum_cohere, school_params.cohere_k)

    def _shoal(self, school_params: SchoolParameters, world_width: float) -> None:
        direct_d: float = self.position.distance_to(school_params.shoal_location)
        wrap_shoal_pos: Vector2 = school_params.shoal_location + Vector2(world_width, 0) if school_params.shoal_location.x < (
                    world_width / 2) else school_params.shoal_location - Vector2(world_width, 0)
        wrap_d: float = self.position.distance_to(wrap_shoal_pos)
        d: float = direct_d
        shoal_pos: Vector2 = school_params.shoal_location
        if wrap_d < direct_d:
            d = wrap_d
            shoal_pos = wrap_shoal_pos
        diff = shoal_pos - self.position
        if d > school_params.shoal_radius:
            self.target(diff, school_params.shoal_k)
        else:
            self.target(diff, -school_params.shoal_k)

    def get_surface(self):
        """
        Gets the surface of this entity rotated according to its velocity.\n
        This function is currently the most expensive thing being done when drawing the screen and will tank FPS if there are too many fish to display at once
        """
        return pygame.transform.rotate(
            self.sprite, math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        )
