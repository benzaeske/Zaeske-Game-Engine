import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2, Rect

from model.entity.entity import Entity
from model.player.camera import Camera
from model.world.gridspace.grid_cell import GridCell
from model.world.gridspace.gridspaceinterface import GridSpaceInterface


class GridSpace(GridSpaceInterface):
    def __init__(self, cell_size: float) -> None:
        super().__init__()
        self._cell_size: float = cell_size
        self._grid: dict[Tuple[int, int], GridCell] = {}

    def get_grid_cell_coord_from_position(self, p: Vector2) -> Tuple[int, int]:
        return int(p.y // self._cell_size), int(p.x // self._cell_size)

    def add_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        self.add_entity_at_coord(coord, entity)

    def add_entity_at_coord(self, coord: Tuple[int, int], entity: Entity) -> None:
        if coord not in self._grid:
            self._grid[coord] = GridCell(coord)
        self._grid[coord].add_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        self.remove_entity_at_coord(coord, entity)

    def remove_entity_at_coord(self, coord: Tuple[int, int], entity: Entity) -> None:
        if coord in self._grid:
            self._grid[coord].remove_entity(entity)
        else:
            raise ValueError(f"Attempting to remove entity at coordinate that is not in loaded grid space: {coord}")

    def get_grid_cell(self, p: Vector2) -> GridCell | None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(p)
        if coord in self._grid:
            return self._grid[coord]
        else:
            return None

    def get_grid_cells_in_camera_range(self, camera: Camera) -> list[GridCell]:
        grid_cells: list[GridCell] = []
        window: Rect = camera.get_window()
        bottom: int = int(window.top // self._cell_size) # Pygame Rect has inverted y coordinates
        top: int = int(window.bottom // self._cell_size) # Pygame Rect has inverted y coordinates
        left: int = int(window.left // self._cell_size)
        right: int = int(window.right // self._cell_size)
        for row in range(bottom, top + 1):
            for col in range(left, right + 1):
                if (row, col) in self._grid:
                    grid_cells.append(self._grid[(row, col)])
        return grid_cells

    def get_neighbors_for_entity(self, entity: Entity, cell_range: int, manager_ids: set[UUID] | None = None) -> list[Entity]:
        if manager_ids is None:
            manager_ids = set()
            manager_ids.add(entity.get_manager_id())
        return self.get_neighbors(entity.get_position(), cell_range, manager_ids)

    def get_neighbors(self, p: Vector2, cell_range: int, manager_ids: set[UUID]) -> list[Entity]:
        neighbors: list[Entity] = []
        r: int = int(p.y / self._cell_size)
        c: int = int(p.x / self._cell_size)
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

    # TODO remove after refactor
    def generate_random_background_noise(self, coord: Tuple[int, int]):
        background: Surface = pygame.Surface((self._cell_size, self._cell_size))
        noise: int = random.randint(0, 25)
        if coord[0] == 0:
            background.fill((99, 85, 52))
        else:
            background.fill((0, 50 + noise, 115 + noise * 2))