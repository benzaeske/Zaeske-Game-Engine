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
        self, others: list["Fish"], school_params: SchoolParameters
    ) -> None:
        self._school(others, school_params)
        if school_params.shoal_location is not None:
            self._shoal(school_params)

    def _school(self, others: list["Fish"], school_params: SchoolParameters) -> None:
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
            if self.school_id == other.school_id:
                # TODO add check to make sure not to check this entity against itself
                d: float = self.position.distance_to(other.position)
                if (d > 0) and d < school_params.cohere_distance:
                    sum_align += other.velocity
                    sum_cohere += other.position
                    count_n += 1
                if (d > 0) and (d < school_params.avoid_distance):
                    diff: Vector2 = self.position - other.position
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

    def _shoal(self, school_params: SchoolParameters) -> None:
        diff = school_params.shoal_location - self.position
        d = self.position.distance_to(school_params.shoal_location)
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
