import random
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Surface, Vector2

from model.entities.gameentity import GameEntity
from model.world.grid_cell import GridCell
from model.world.worldspecs import WorldSpecs


class GridSpace:
    """
    Grid space representing all GridCells in the world space as a dictionary where keys are integer row/col coordinates

    Should eventually be refactored to only store grid cells within a certain range of the player's location and load/unload them from the dictionary when the player moves grid cells:

    The map background should eventually be represented as chunks that store 32x32 configurations of background tiles that are the same size as a single GridCell.
    There are a fixed number of preloaded chunks that the world can be built out of. The map background will be a 2d array or dictionary that stores unique ids for these preloaded chunks
    When drawing the background for a grid cell a simple lookup to the chunk/tile gets the background to draw.
    On player movement, when loading new grid cells into the dictionary, the only thing that needs to be instantiated is the coordinate of the grid cell in the larger grid space, and an empty
    dictionary for storing entity id's of entities that move into that grid cell.
    Entities that move outside the range of loaded grid cells should either be wrapped to the other side or deleted. Similarly, entities that are in grid cells
    that get unloaded should wrap/delete accordingly

    Side note: Some grid cells/chunks might want entities preloaded into them (events, NPCs, item pickups etc). These can easily be represented in a separate dictionary
    of 'preloaded things' where keys are grid cell coordinates. When a grid cell gets loaded a simple lookup to this map will add the necessary objects if they exist with negligible overhead

    Side note 2: Will this support a large enough map?
    Assume chunks are 32x32 grid cells. Grid cells are size 128x128 pygame Surfaces.
    If the map is 128x128 chunks then we are storing a dictionary of: 16,384 integers to represent the map which is not that large (in the order of a single MB)
    If the turtle can cross a grid cell in half a second (the speed used in the alpha) then the turtle can cross a chunk in 16 seconds.
    This means it would take the turtle 16 seconds x 128 chunks = 2048 seconds / 60 seconds in one minute = ~34 minutes to cross the map in a single
    direction.
    """
    def __init__(self, world_specs: WorldSpecs) -> None:
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

    def add_entity(self, entity: GameEntity, coord: Tuple[int, int] = None) -> None:
        if coord is None:
            coord = self.get_grid_cell_coord_from_position(entity.position.x, entity.position.y)
        if coord in self._grid:
            self._grid[coord].add_entity(entity)
        else:
            raise ValueError(f"Attempting to add entity at coordinate that is not in loaded grid space: {coord}")

    def remove_entity(self, entity: GameEntity, coord: Tuple[int, int] = None) -> None:
        if coord is None:
            coord = self.get_grid_cell_coord_from_position(entity.position.x, entity.position.y)
        if coord in self._grid:
            self._grid[coord].remove_entity(entity)
        else:
            raise ValueError(f"Attempting to remove entity at coordinate that is not in loaded grid space: {coord}")

    def get_grid_cell_coord_from_position(self, x: float | int, y: float | int) -> Tuple[int, int]:
        return int(y / self.cell_size), int(x / self.cell_size)

    def get_grid_cell(self, coord: Tuple[int, int]) -> GridCell:
        return self._grid[coord]

    def get_surrounding_cells(self, center_cell_coord: Tuple[int, int], cell_range: int) -> list[GridCell]:
        surrounding_cells: list[GridCell] = []
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = center_cell_coord[0] + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = center_cell_coord[1] + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                surrounding_cells.append(self._grid[(grid_r, grid_c)])
        return surrounding_cells

    def get_entity_neighbors(self, entity: GameEntity, cell_range: int, group_ids: set[UUID] = None) -> list[GameEntity]:
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
            group_ids.add(entity.group_id)
        return self.get_neighbors(entity.position.x, entity.position.y, cell_range, group_ids)

    def get_neighbors(self, x: float, y: float, cell_range: int, group_ids: set[UUID]) -> list[GameEntity]:
        neighbors: list[GameEntity] = []
        r: int = int(y / self.cell_size)
        c: int = int(x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                for group_id in group_ids:
                    neighbors.extend(self._grid[(grid_r, grid_c)].get_entities_by_group_id(group_id))
        return neighbors

    def process_moved_entity(self, old_position: Vector2, entity: GameEntity) -> None:
        """
        Checks if a given entity needs to move the grid cell it is contained in after it has undergone movement for the current frame.
        Should only be called after all movement has been processed for an entity.
        :param old_position: The position of the entity before moving this frame
        :param entity: The current GameEntity object
        """
        old_coord = self.get_grid_cell_coord_from_position(old_position.x, old_position.y)
        current_coord = self.get_grid_cell_coord_from_position(entity.position.x, entity.position.y)
        if old_coord != current_coord:
            self.remove_entity(entity, old_coord)
            self.add_entity(entity, current_coord)


