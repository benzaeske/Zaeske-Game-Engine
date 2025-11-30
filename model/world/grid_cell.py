import pygame
from pygame import Surface, Vector2

from model.entities.fish.fish import Fish


class GridCell:
    def __init__(
        self,
        size: float,
        row: int,
        col: int,
        background_surface: Surface = None,
    ):
        self.size: float = size
        self.fish: list[Fish] = []
        if background_surface is None:
            self.background_surface: Surface = pygame.Surface((size, size))
            self.background_surface.fill((0, 0, 0))
        else:
            self.background_surface: Surface = background_surface
        self.center_pos: Vector2 = Vector2(
            col * size + (size / 2), row * size + (size / 2)
        )
