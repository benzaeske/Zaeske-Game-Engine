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
                coord: Tuple[int, int] = (row, col)
                background: Surface = pygame.Surface((self.cell_size, self.cell_size))
                noise: int = random.randint(0, 25)
                if row == 0:
                    background.fill((99, 85, 52))
                else:
                    background.fill((0, 50 + noise, 115 + noise * 2))
                new_grid[coord] = GridCell(coord, background)
        return new_grid

    def get_grid_cell_coord_from_position(self, p: Vector2) -> Tuple[int, int]:
        return int(p.y / self.cell_size), int(p.x / self.cell_size)

    def add_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        if coord in self._grid:
            self._grid[coord].add_entity(entity)
        else:
            raise ValueError(f"Attempting to add entity at coordinate that is not in loaded grid space: {coord}")

    def remove_entity(self, entity: Entity) -> None:
        coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
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
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                neighbors.extend(self._grid[(grid_r, grid_c)].get_entities_by_manager_ids(manager_ids))
        return neighbors

    def process_moved_entity(self, old_position: Vector2, entity: Entity) -> None:
        old_coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(old_position)
        current_coord: Tuple[int, int] = self.get_grid_cell_coord_from_position(entity.get_position())
        if old_coord != current_coord:
            self._grid[old_coord].remove_entity(entity)
            self._grid[current_coord].add_entity(entity)

    def get_entity_neighbors(self, entity: Entity, cell_range: int, group_ids: set[UUID] | None = None) -> list[Entity]:
        """
        Gets all neighbor entities relative to the input entity.
        Neighbors are considered any entity in a grid cell within the square region bounded by the input cell_range.
        :param entity: The entity to find neighbors for
        :param cell_range: The square cell range around which to look for neighbors
        :param group_ids: The group ids of entities that are considered neighbors. If no group_ids are passed in the group_id of the input entity is used
        :return: a list of GameEntities that neighbor the input entity
        """
        if group_ids is None:
            group_ids = set()
            group_ids.add(entity.get_manager_id())
        return self.get_neighbors(entity.get_x(), entity.get_y(), cell_range, group_ids)

    def get_neighbors(self, x: float, y: float, cell_range: int, group_ids: set[UUID]) -> list[Entity]:
        neighbors: list[Entity] = []
        r: int = int(y / self.cell_size)
        c: int = int(x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                for group_id in group_ids:
                    neighbors.extend(self._grid[(grid_r, grid_c)].get_entities_by_manager_id(group_id))
        return neighbors

    def process_moved_entity(self, old_position: Vector2, entity: Entity) -> None:
        """
        Checks if a given entity needs to move the grid cell it is contained in after it has undergone movement for the current frame.
        Should only be called after all movement has been processed for an entity.
        :param old_position: The position of the entity before moving this frame
        :param entity: The current GameEntity object
        """
        old_coord = self.get_grid_cell_coord_from_position(old_position.x, old_position.y)
        current_coord = self.get_grid_cell_coord_from_position(entity.get_x(), entity.get_y())
        if old_coord != current_coord:
            self.remove_entity(entity, old_coord)
            self.add_entity(entity, current_coord)





