from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.entitygroup import EntityGroup
from model.entities.fish.fish import Fish
from model.entities.jellyfish.jellyfish import Jellyfish


class GridCell:
    """
    An individual grid cell in the model's grid space.\n
    Currently stores the fish that are within its boundaries as well as a random blue background color.\n
    The view draws background based on the grid cells that are within the player's camera range
    """

    def __init__(
        self,
        size: float,
        row: int,
        col: int,
        background_surface: Surface = None,
    ):
        self.size: float = size
        self.fish: dict[UUID, Fish] = {}
        self.jellyfish: dict[UUID, Jellyfish] = {}
        self.entity_groups: dict[UUID, EntityGroup] = {}
        if background_surface is None:
            self.background_surface: Surface = pygame.Surface((size, size))
        else:
            self.background_surface: Surface = background_surface
        self.center_pos: Vector2 = Vector2(
            col * size + (size / 2), row * size + (size / 2)
        )
