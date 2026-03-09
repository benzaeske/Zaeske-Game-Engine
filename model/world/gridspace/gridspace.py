import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.entity import Entity
from model.world.gridspace.grid_cell import GridCell
from model.world.gridspace.gridspaceinterface import GridSpaceInterface
from model.world.worldspecs import WorldSpecs


class GridSpace(GridSpaceInterface):
    def __init__(self, world_specs: WorldSpecs) -> None:
        super().__init__()
        self.cell_size: float = world_specs.cell_size
        self.grid_width: int = world_specs.grid_width
        self.grid_height: int = world_specs.grid_height
        self._grid: dict[Tuple[int, int], GridCell] = self.initialize_grid_space()

    def initialize_grid_space(self) -> dict[Tuple[int, int], GridCell]:
        new_grid: dict[Tuple[int, int], GridCell] = {}
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                new_grid[(row, col)] = self.get_new_grid_cell((row, col))
        return new_grid

    def get_new_grid_cell(self, coord: Tuple[int, int]) -> GridCell:
        background: Surface = pygame.Surface((self.cell_size, self.cell_size))
        noise: int = random.randint(0, 25)
        if coord[0] == 0:
            background.fill((99, 85, 52))
        else:
            background.fill((0, 50 + noise, 115 + noise * 2))
        return GridCell(coord, background)

    def get_grid_cell_coord_from_position(self, p: Vector2) -> Tuple[int, int]:
        return int(p.y / self.cell_size), int(p.x / self.cell_size)

    def add_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        self.add_entity_at_coord(coord, entity)

    def add_entity_at_coord(self, coord: Tuple[int, int], entity: Entity) -> None:
        if coord not in self._grid:
            self._grid[coord] = self.get_new_grid_cell(coord)
        self._grid[coord].add_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        self.remove_entity_at_coord(coord, entity)

    def remove_entity_at_coord(self, coord: Tuple[int, int], entity: Entity) -> None:
        if coord in self._grid:
            self._grid[coord].remove_entity(entity)
        else:
            raise ValueError(f"Attempting to remove entity at coordinate that is not in loaded grid space: {coord}")

    def get_grid_cell(self, p: Vector2) -> GridCell:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(p)
        if coord in self._grid:
            return self._grid[coord]
        else:
            raise ValueError("Attempting to get a grid cell that is not in loaded grid space")

    def get_neighbors_for_entity(self, entity: Entity, cell_range: int, manager_ids: set[UUID] | None = None) -> list[Entity]:
        if manager_ids is None:
            manager_ids = set()
            manager_ids.add(entity.get_manager_id())
        return self.get_neighbors(entity.get_position(), cell_range, manager_ids)

    def get_neighbors(self, p: Vector2, cell_range: int, manager_ids: set[UUID]) -> list[Entity]:
        neighbors: list[Entity] = []
        r: int = int(p.y / self.cell_size)
        c: int = int(p.x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_c: int = c + dc
                if (grid_r, grid_c) in self._grid:
                    neighbors.extend(self._grid[(grid_r, grid_c)].get_entities_by_manager_ids(manager_ids))
        return neighbors

    def process_moved_entity(self, old_position: Vector2, entity: Entity) -> None:
        old_coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(old_position)
        current_coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        if old_coord != current_coord:
            self.remove_entity_at_coord(old_coord, entity)
            self.add_entity_at_coord(current_coord, entity)