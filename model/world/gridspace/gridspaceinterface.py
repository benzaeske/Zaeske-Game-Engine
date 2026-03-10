from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from uuid import UUID

from pygame import Vector2

from model.player.camera import Camera
from model.world.gridspace.grid_cell import GridCell

if TYPE_CHECKING:
    from model.entities.entity import Entity


class GridSpaceInterface(ABC):
    """
    Defines publicly accessible functionality for the grid space.
    """
    def __init__(self):
        pass

    @abstractmethod
    def add_entity(self, entity: Entity) -> None:
        """
        Adds the provided entity into the grid space based on its position.
        :param entity: the entity to add
        """
        pass

    @abstractmethod
    def remove_entity(self, entity: Entity) -> None:
        """
        Removes the provided entity from the grid space.
        :param entity: the entity to remove
        """
        pass

    @abstractmethod
    def get_grid_cell(self, p: Vector2) -> GridCell:
        """
        :param p: A vector representing a point in grid space.
        :return: The grid cell that contains the provided point.
        """
        pass

    @abstractmethod
    def get_grid_cells_in_camera_range(self, camera: Camera) -> list[GridCell]:
        """
        Returns a list of all grid cells that are visible within the provided camera's boundaries.
        """
        pass

    @abstractmethod
    def get_neighbors_for_entity(self, entity: Entity, cell_range: int, manager_ids: set[UUID] | None = None) -> list[Entity]:
        """
        Returns all neighboring entities relative to the input entity's position. Neighbors are considered any entity
        in a grid cell within the square region bounded by the input cell_range.
        :param entity: The entity to get neighbors for
        :param cell_range: The range of grid cells to look for neighbors
        :param manager_ids: Only entities belonging to these managers will be returned. If None, will use the manager
            id of the input entity
        :return: A list of Entities
        """
        pass

    @abstractmethod
    def get_neighbors(self, p: Vector2, cell_range: int, manager_ids: set[UUID]) -> list[Entity]:
        """
        Returns all neighboring entities relative to the input point. A neighboring entity is an entity that is
        contained in a grid cell within the square region defined by the input cell_range. Only entities that
        belong to the provided manager_ids are returned.
        :param p: The point in grid space that will be searched around to find neighbors
        :param cell_range: The range of grid cells to look for neighbors
        :param manager_ids: Only entities belonging to these managers will be returned
        :return: A list of Entities
        """
        pass

    @abstractmethod
    def process_moved_entity(self, old_position: Vector2, entity: Entity) -> None:
        """
        Used to move an entity to a new grid cell if it changed positions this frame.
        :param old_position: The position of the entity before it moved this frame
        :param entity: The entity in its current position after moving this frame
        """
        pass